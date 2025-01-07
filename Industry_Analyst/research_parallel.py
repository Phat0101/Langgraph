from dotenv import load_dotenv
import os
import json
import asyncio
from tavily import TavilyClient, AsyncTavilyClient
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.tools import tool
from langchain_core.runnables import RunnableConfig
from langgraph.graph import StateGraph, END
from langgraph.constants import Send
from langsmith import Client, traceable
from typing import List, Optional, Literal, Annotated, Dict


# Import state and prompts
from Industry_Analyst.state import (
# from state import (
    ResearchState, ResearchStateInput, ResearchStateOutput,
    AnalystState, AnalystOutputState, ResearchPlan, Reflection,
    IndustryData
)
from Industry_Analyst.prompts import (
# from prompts import (
    RESEARCH_PLAN_PROMPT, ANALYSIS_PROMPT, SUMMARY_PROMPT,
    REFLECTION_PROMPT, COMBINE_SUMMARIES_PROMPT
)

# Environment setup
load_dotenv()
api_key = os.getenv("GOOGLE_GENERATIVE_AI_API_KEY")
tavily_api_key = os.getenv("TAVILY_API_KEY")
langsmith_api_key = os.getenv("LANGCHAIN_API_KEY")

# Client initialization
tavily_client = TavilyClient(api_key=tavily_api_key)
tavily_async_client = AsyncTavilyClient(api_key=tavily_api_key)
langsmith_client = Client()

# LLM Configuration
model = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    google_api_key=api_key,
    temperature=0.7,
)

# Helper Functions for Source Management
def deduplicate_and_format_sources(search_response, max_tokens_per_source, include_raw_content=True):
    """
    Takes either a single search response or list of responses from Tavily API and formats them.
    Limits the raw_content to approximately max_tokens_per_source.
    include_raw_content specifies whether to include the raw_content from Tavily in the formatted string.
    
    Args:
        search_response: Either:
            - A dict with a 'results' key containing a list of search results
            - A list of dicts, each containing search results
            
    Returns:
        str: Formatted string with deduplicated sources
    """
    # Convert input to list of results
    if isinstance(search_response, dict):
        sources_list = search_response['results']
    elif isinstance(search_response, list):
        sources_list = []
        for response in search_response:
            if isinstance(response, dict) and 'results' in response:
                sources_list.extend(response['results'])
            else:
                sources_list.extend(response)
    else:
        raise ValueError("Input must be either a dict with 'results' or a list of search results")
    
    # Deduplicate by URL
    unique_sources = {}
    for source in sources_list:
        if source['url'] not in unique_sources:
            unique_sources[source['url']] = source
    
    # Format output
    formatted_text = "Sources:\n\n"
    for i, source in enumerate(unique_sources.values(), 1):
        formatted_text += f"Source {source['title']}:\n===\n"
        formatted_text += f"URL: {source['url']}\n===\n"
        formatted_text += f"Most relevant content from source: {source['content']}\n===\n"
        if include_raw_content:
            # Using rough estimate of 4 characters per token
            char_limit = max_tokens_per_source * 4
            # Handle None raw_content
            raw_content = source.get('raw_content', '')
            if raw_content is None:
                raw_content = ''
                # print(f"Warning: No raw_content found for source {source['url']}")
            if len(raw_content) > char_limit:
                raw_content = raw_content[:char_limit] + "... [truncated]"
            formatted_text += f"Full source content limited to {max_tokens_per_source} tokens: {raw_content}\n\n"
                
    return formatted_text.strip()

# Tavily Search Tool
@traceable
async def tavily_search_async(query: str) -> str:
    """Search the web using the Tavily API asynchronously.
    
    Args:
        query (str): The search query to execute
        
    Returns:
        str: JSON string containing search results or error message
    """
    if not query:
        return json.dumps({"error": "No search query provided"}, ensure_ascii=False)
    
    try:
        search_result = await tavily_async_client.search(
            query,
            search_depth="advanced",
            max_results=5,
            include_answer=True,
            include_raw_content=True
        )
        return json.dumps(search_result, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"error": f"Error performing search: {str(e)}"}, ensure_ascii=False)

# Agent Functions
def research_planner(state: ResearchState):
    planner = model.with_structured_output(ResearchPlan)
    prompt = RESEARCH_PLAN_PROMPT.format(topic=state.topic)
    plan = planner.invoke([HumanMessage(content=prompt)])
    
    # Limit the number of search queries to 5 to avoid halucination
    limited_search_queries = plan.search_queries[:5]
    
    return {
        "plan": plan,
        "search_queries": limited_search_queries,
        "search_query": limited_search_queries[0],
        "research_loop_count": 0
    }

async def industry_analyst(state: AnalystState, config: RunnableConfig):
    # Search and analyze
    raw_results = await tavily_search_async(state.search_query)
    # Parse JSON string to dict
    search_results = json.loads(raw_results)
    formatted_results = deduplicate_and_format_sources(search_results, 10000)
    
    # Add a helper function to format sources
    def format_sources(search_results):
        """Format search results into bulleted list"""
        return '\n'.join(
            f"* {result['title']}: {result['url']}"
            for result in search_results['results']
        )
    
    analyst = model.with_structured_output(IndustryData)
    analysis_prompt = ANALYSIS_PROMPT.format(
        query=state.search_query,
        formatted_results=formatted_results
    )
    analysis = analyst.invoke([HumanMessage(content=analysis_prompt)])
    
    # Generate running summary
    current_summaries = state.running_summaries or []
    latest_summary = current_summaries[-1] if current_summaries else ""
    
    summary_prompt = SUMMARY_PROMPT.format(
        current_summary=latest_summary,
        analysis=formatted_results
    )
    summary = model.invoke([HumanMessage(content=summary_prompt)])
    
    return {
        "web_research_results": [formatted_results],
        "sources_gathered": [format_sources(search_results)],
        "running_summaries": [summary.content],
        "research_loop_count": state.research_loop_count + 1,
        "analyses": [analysis]  # Return as list for parallel aggregation
    }

def should_continue_research(state: AnalystState) -> Literal["reflect", "end_analysis"]:
    """Determine if more research is needed"""
    if state.research_loop_count < 2:  # Maximum 2 or 3 iterations per query, can be adjusted
        return "reflect"
    return "end_analysis"

def reflect_on_research(state: AnalystState):
    """Reflect on current findings and possibly refine or repeat the same search query."""
    # Get the latest summary from the list
    current_summary = state.running_summaries[-1] if state.running_summaries else ""
    
    reflection_prompt = REFLECTION_PROMPT.format(
        query=state.search_query,
        current_summary=current_summary
    )
    reflection_agent = model.with_structured_output(Reflection)
    reflection = reflection_agent.invoke([HumanMessage(content=reflection_prompt)])
    refined_query = reflection.refined_query

    # If reflection indicates the current query is sufficient, move to the next search query
    if reflection.sufficient:
        return {"search_query": state.search_query, "research_loop_count": 2} # Set to max loop count to end analysis
    else:
        # Use refined query to run additional iteration on the same index
        return {"search_query": refined_query, "research_loop_count": state.research_loop_count}

def end_analysis(state: AnalystState) -> AnalystOutputState:
    """End the analysis for the current query and prepare output"""
    return {
        "completed_analyses": state.analyses,  # Changed from single analysis
        "sources_gathered": state.sources_gathered,
        "running_summaries": state.running_summaries
    }

def initiate_analysis(state: ResearchState):
    """Initiate analysis for each query in parallel"""
    return [
        Send("analyst", {
            "search_query": query,
            "research_loop_count": 0,
            "running_summaries": [],  # Initialize empty list for summaries
            "sources_gathered": state.sources_gathered
        })
        for query in state.search_queries 
    ]

def aggregate_analyses(state: ResearchState) -> Dict:
    """Lead Analyst Agent writes the final report"""
    """Aggregate analyses from parallel runs"""
    
    # Clean and deduplicate sources
    all_sources = set()
    for sources in state.sources_gathered:
        cleaned_sources = [
            source.strip().replace('\n', ' ').replace('\r', '')
            for source in sources.split('*')
            if source.strip()
        ]
        all_sources.update(cleaned_sources)
    
    # Combine all analyses into a comprehensive industry data object
    combined_analysis = IndustryData(
        # news=[news for analysis in state.completed_analyses for news in analysis.news],
        # projections=[proj for analysis in state.completed_analyses for proj in analysis.projections],
        # risks=[risk for analysis in state.completed_analyses for risk in analysis.risks],
        # competitors=[comp for analysis in state.completed_analyses for comp in analysis.competitors]
        overview = state.completed_analyses[-1].overview,
        classification = state.completed_analyses[-1].classification,
        metrics = state.completed_analyses[-1].metrics,
        porters_forces = [force for analysis in state.completed_analyses for force in analysis.porters_forces],
        trends = [trend for analysis in state.completed_analyses for trend in analysis.trends],
        news = [news for analysis in state.completed_analyses for news in analysis.news],
        projections = [proj for analysis in state.completed_analyses for proj in analysis.projections],
        risks = [risk for analysis in state.completed_analyses for risk in analysis.risks],
        competitors = [comp for analysis in state.completed_analyses for comp in analysis.competitors]
    )
    
    # Combine all summaries into a single coherent summary
    combined_summary = model.invoke([
        HumanMessage(content=COMBINE_SUMMARIES_PROMPT.format(
            summaries=' '.join(state.running_summaries),
            combined_analysis=combined_analysis,
            topic=state.topic
        ))
    ]).content
    
    return {
        "completed_analyses": [combined_analysis],
        "sources_gathered": [f"* {source}" for source in all_sources if source],  # Format sources consistently
        "running_summaries": [combined_summary]
    }

def finalize_report(state: ResearchState):
    """Format and finalize the research report"""

    formatted_sources = '\n'.join(
        source.strip()
        for source in state.sources_gathered
        if source.strip()
    )
    
    final_summary = state.running_summaries[-1] if state.running_summaries else "No analysis available"
    report = f"## Analysis Report\n\n{final_summary}\n\n### Sources:\n{formatted_sources}"
    
    return {"final_report": report,
            "completed_analyses": state.completed_analyses}

# Parallel analyst_workflow 
analyst_workflow = StateGraph(AnalystState, output=AnalystOutputState)
analyst_workflow.add_node("analyst", industry_analyst)
analyst_workflow.add_node("reflect", reflect_on_research)
analyst_workflow.add_node("end_analysis", end_analysis)
analyst_workflow.set_entry_point("analyst")
analyst_workflow.add_conditional_edges(
    "analyst",
    should_continue_research,
    {
        "reflect": "reflect",
        "end_analysis": "end_analysis"
    }
)
analyst_workflow.add_edge("reflect", "analyst")
analyst_workflow.add_edge("end_analysis", END)
compiled_analyst = analyst_workflow.compile()

# Main Graph Definition
workflow = StateGraph(ResearchState, input=ResearchStateInput, output=ResearchStateOutput)
workflow.add_node("research_planner", research_planner)
workflow.add_node("analyst", compiled_analyst)
workflow.add_node("aggregate_analyses", aggregate_analyses)
workflow.add_node("finalize", finalize_report)

workflow.set_entry_point("research_planner")
workflow.add_conditional_edges("research_planner", initiate_analysis, ["analyst"])
workflow.add_edge("analyst", "aggregate_analyses")
workflow.add_edge("aggregate_analyses", "finalize")
workflow.add_edge("finalize", END)

graph = workflow.compile()

# # Update the execution to use async
# async def analyze_industry(topic: str):
#     """Async function to analyze an industry"""
#     result = await graph.ainvoke({
#         "topic": topic
#     })
#     return result

# # Example usage
# if __name__ == "__main__":
#     import asyncio
    
#     async def main():
#         result = await analyze_industry("Research Palantir Stock Industry about Competitors, Risks and Growth projection for the industry") 
#         print("Final Report:")
#         print(result["final_report"])
    
#     asyncio.run(main())