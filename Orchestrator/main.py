from dotenv import load_dotenv
import os
from fastapi import APIRouter, HTTPException
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph, END
from langgraph.constants import Send
from langchain_core.runnables import RunnableConfig
from langsmith import Client, traceable
from typing import List, Optional, Literal, Annotated, Dict

from backend.routers.Economic_Analyst.economic_analyst import graph as economic_graph
from backend.routers.Economic_Analyst.state import ResearchStateOutput as EconomicResearchStateOutput

from backend.routers.Industry_Analyst.research_parallel import graph as industry_graph
from backend.routers.Industry_Analyst.state import ResearchStateOutput as IndustryResearchStateOutput

from backend.routers.Quantitative_Analyst.quantitative_analyst import graph as quantitative_graph
from backend.routers.Quantitative_Analyst.state import QuantAnalystOutput as QuantitativeAnalystOutput

from backend.routers.Orchestrator.state import OrchestratorState, OrchestratorInput, OrchestratorOutput, OrchestratorPlan, CombinedAnalysis
from backend.routers.Orchestrator.prompts import ORCHESTRATOR_PLAN_PROMPT, COMBINE_ANALYSES_PROMPT

# Environment setup
load_dotenv()
api_key = os.getenv("GOOGLE_GENERATIVE_AI_API_KEY")
langsmith_api_key = os.getenv("LANGCHAIN_API_KEY")
langsmith_client = Client()

if not api_key:
    raise ValueError("GOOGLE_GENERATIVE_AI_API_KEY environment variable is not set")

# LLM Configuration
model = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash-exp",
    google_api_key=api_key,
    temperature=0.7,
)

def create_research_plan(state: OrchestratorState):
    """Create research plans for both analyses"""
    orchestrator = model.with_structured_output(OrchestratorPlan)
    prompt = ORCHESTRATOR_PLAN_PROMPT.format(stock=state.stock)
    plan = orchestrator.invoke([HumanMessage(content=prompt)])
    
    return {
        "plan": plan,
        "web_research_results": [],
        "sources_gathered": [],
        "running_summaries": [],
        "completed_analyses": []
    }

def initiate_analyses(state: OrchestratorState):
    """Launch both analyses in parallel"""
    return [
        Send("economic_analysis", {"topic": state.plan.economic_query}),
        Send("industry_analysis", {"topic": state.plan.industry_query}),
        Send("quantitative_analysis", {"stock": state.stock})
    ]

def combine_analyses(state: OrchestratorState, config: Optional[RunnableConfig] = None) -> Dict:
    """Combine results from both analyses"""
    # Gather completed final reports
    
    final_economic_report = state.final_economic_report[-1]
    final_industry_report = state.final_industry_report[-1]
    final_quantitative_report = state.final_quantitative_report[-1]
    
    # Generate combined analysis
    prompt = COMBINE_ANALYSES_PROMPT.format(
        economic_analysis=final_economic_report,
        industry_analysis=final_industry_report,
        quantitative_analysis=final_quantitative_report,
        stock=state.stock
    )
    
    final_analysis = model.invoke([HumanMessage(content=prompt)])
    
    return {
        "final_report": final_analysis.content,
    }

# Main Graph Definition
workflow = StateGraph(OrchestratorState, input=OrchestratorInput, output=OrchestratorOutput)

# Add nodes
workflow.add_node("orchestrator", create_research_plan)
workflow.add_node("economic_analysis", economic_graph)
workflow.add_node("industry_analysis", industry_graph)
workflow.add_node("quantitative_analysis", quantitative_graph)
workflow.add_node("combine", combine_analyses)

# Connect nodes
workflow.set_entry_point("orchestrator")
workflow.add_conditional_edges("orchestrator", initiate_analyses, ["economic_analysis", "industry_analysis", "quantitative_analysis"])

# Results feed directly into combine
workflow.add_edge("economic_analysis", "combine")
workflow.add_edge("industry_analysis", "combine")
workflow.add_edge("quantitative_analysis", "combine")
workflow.add_edge("combine", END)

# Compile graph
graph = workflow.compile()

# # FastAPI Router
# router = APIRouter(
#     prefix="/ai",
#     tags=["ai"],
#     responses={404: {"description": "Not found"}},
# )

# @router.get("/analyze/{stock}")
# async def analyze_stock(stock: str):
#     """Perform comprehensive stock analysis."""
#     try:
#         result = await graph.ainvoke({
#             "stock": stock
#         })
#         return result
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
