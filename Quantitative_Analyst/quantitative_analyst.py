from dotenv import load_dotenv
import os
import requests
import json
import asyncio
from tavily import AsyncTavilyClient
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.tools import tool
from langchain_core.runnables import RunnableConfig
from langgraph.graph import StateGraph, END
# from langgraph.prebuilt import create_react_agent
from langsmith import Client, traceable
from typing import List, Optional, Literal, Annotated, Dict, Union

from backend.routers.Quantitative_Analyst.state import (
    QuantAnalystState, QuantAnalystInput, QuantAnalystOutput,
    # FinancialMetrics,
    Reflection,
    ResearchPlan
)
from backend.routers.Quantitative_Analyst.prompts import (
    SYMBOL_REFLECTION_PROMPT, FINANCIAL_ANALYSIS_PROMPT
)

load_dotenv()
api_key = os.getenv("GOOGLE_GENERATIVE_AI_API_KEY")
langsmith_api_key = os.getenv("LANGCHAIN_API_KEY")
quickfs_api_key = os.getenv("QUICKFS_API_KEY")

if not api_key:
    raise ValueError("GOOGLE_GENERATIVE_AI_API_KEY environment variable is not set")
if not langsmith_api_key:
    raise ValueError("LANGCHAIN_API_KEY environment variable is not set")

model = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    google_api_key=api_key,
    temperature=0.3,
)

quant = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash-exp",
    google_api_key=api_key,
    temperature=0.5,
)

def flatten_json(data: Dict, parent_key: str = "", sep: str = "_") -> Dict:
    """Flattens a nested JSON dictionary."""
    items = []
    for key, value in data.items():
        new_key = parent_key + sep + key if parent_key else key
        if isinstance(value, dict):
            items.extend(flatten_json(value, new_key, sep=sep).items())
        elif isinstance(value, list):
            for i, list_item in enumerate(value):
                if isinstance(list_item, dict):
                    items.extend(
                        flatten_json(list_item, f"{new_key}{sep}{i}", sep=sep).items()
                    )
                else:
                    items.append((f"{new_key}{sep}{i}", list_item))
        else:
            items.append((new_key, value))
    return dict(items)

def format_json_for_llm(
    data: Union[Dict, List],
    task_description: str,
    delimiter_start: str = "BEGIN_JSON",
    delimiter_end: str = "END_JSON",
    flatten_nested: bool = False,
    exclude_keys: List[str] = None,
) -> str:
    """Formats a JSON object for an LLM prompt

    Args:
        data: A Python dictionary or list (or data that can be converted to JSON).
        task_description: A string describing what the LLM should do with the data.
        delimiter_start: String to use as the start delimiter.
        delimiter_end: String to use as the end delimiter.
        flatten_nested: Whether to flatten nested JSON structures (default: False).
        exclude_keys: List of keys to remove from the JSON object (default: None).

    Returns:
        A string containing a prompt with the formatted JSON.
    """
    if exclude_keys:
        if isinstance(data, dict):
            data = {k: v for k, v in data.items() if k not in exclude_keys}
        elif isinstance(data, list):
            new_list = []
            for item in data:
                if isinstance(item, dict):
                    new_item = {k: v for k, v in item.items() if k not in exclude_keys}
                    new_list.append(new_item)
            data = new_list

    if flatten_nested:
        if isinstance(data, dict):
            data = flatten_json(data)
        elif isinstance(data, list):
            data = [
                flatten_json(item) if isinstance(item, dict) else item for item in data
            ]

    json_string = json.dumps(
        data, separators=(",", ":"), ensure_ascii=False
    )  # Compact JSON format, support for non-ASCII

    prompt = f"{task_description}\n{delimiter_start}\n{json_string}\n{delimiter_end}"
    return prompt
# Use format_json_for_llm function(data, flatten_nested=False)

@traceable
def get_financial_data(symbol: str):
    """
    Fetches data from the QuickFS API for a given symbol.

    Args:
        symbol (str): The stock symbol (e.g., "AAPL:US" or "CBA:AU").

    Returns:
        dict or None: The JSON response data as a Python dictionary, or None if the request fails.
    """

    url = f"https://public-api.quickfs.net/v1/data/all-data/{symbol}"
    api_key = os.getenv("QUICKFS_API_KEY")

    if not api_key:
        print("Error: QUICKFS_API_KEY not found in environment variables.")
        return None

    headers = {
        "X-QFS-API-Key": api_key
    }

    try:
        response = requests.get(url, headers=headers)
        # if response contains an error in the JSON then return None
        if "errors" in response.json():
            return None
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error during API request: {e}")
        return None
      
def planner(state: QuantAnalystState, config: RunnableConfig):
    """Create a stock name query"""
    planner = model.with_structured_output(ResearchPlan)
    plan = planner.invoke([
        HumanMessage(content=f"Generate a stock symbol to research from {state.stock}")
    ])
    
    return {
        "stock": plan.stock
  }

def retriever(state: QuantAnalystState, config: RunnableConfig):
    """Fetch and analyze financial data"""
    # Try to get data
    data = get_financial_data(state.stock)
    
    if not data:
        return {
            "research_loop_count": state.research_loop_count + 1,
            "symbol_attempts": [state.stock]
        }
    
    formatted_data = format_json_for_llm(
        data,
        task_description="Analyse these financial metrics",
        flatten_nested=True
    )
    
    return {
        "financial_data": formatted_data,
        # "metrics": metrics,
        "research_loop_count": state.research_loop_count + 1
    }

def should_continue_research(state: QuantAnalystState) -> Literal["reflect", "quantitative_analysis"]:
    """Determine if we should try another symbol format"""
    if state.research_loop_count < 3 and not state.financial_data:  # Try up to 3 different formats
        return "reflect"
    return "quantitative_analysis"

def reflect_on_symbol(state: QuantAnalystState):
    """Reflect on failed data fetch and suggest new symbol format"""
    reflection_agent = model.with_structured_output(Reflection)
    reflection = reflection_agent.invoke([
        HumanMessage(content=SYMBOL_REFLECTION_PROMPT.format(
            stock=state.stock,
            symbol=state.symbol_attempts[-1],
            attempt_count=state.research_loop_count,
            previous_attempts=", ".join(state.symbol_attempts)
        ))
    ])
    
    if reflection.sufficient:
        return {"research_loop_count": 3}  # End research
    
    return {
        "stock": reflection.refined_symbol,
        "research_loop_count": state.research_loop_count
    }

def quantitative_analysis(state: QuantAnalystState) -> QuantAnalystOutput:
    """Prepare final output"""
    analysis = quant.invoke([
        HumanMessage(content=FINANCIAL_ANALYSIS_PROMPT.format(
            stock=state.stock,
            formatted_data=state.financial_data
        ))
    ])
    return {
        "final_quantitative_report": [analysis.content],
        # "financial_data": state.financial_data
    }

# Build the graph
workflow = StateGraph(QuantAnalystState, input=QuantAnalystInput, output=QuantAnalystOutput)

# Add nodes
workflow.add_node("planner", planner)
workflow.add_node("retriever", retriever)
workflow.add_node("retry", reflect_on_symbol)
workflow.add_node("quantitative_analysis", quantitative_analysis)

# Connect nodes
workflow.set_entry_point("planner")
workflow.add_edge("planner", "retriever")
workflow.add_conditional_edges(
    "retriever",
    should_continue_research,
    {
        "retry": "retry",
        "quantitative_analysis": "quantitative_analysis"
    }
)
workflow.add_edge("retry", "retriever")
workflow.add_edge("quantitative_analysis", END)

graph = workflow.compile()