from dataclasses import dataclass, field
from typing import List, Optional, Dict, TypedDict, Annotated
from typing_extensions import TypedDict
from pydantic import BaseModel, Field
import operator

from backend.routers.Economic_Analyst.state import EconomicData
from backend.routers.Industry_Analyst.state import IndustryData

class OrchestratorPlan(BaseModel):
    """Plan structure for multi-agent orchestration"""
    economic_query: str = Field(description="Query for economic analysis", default="")
    industry_query: str = Field(description="Query for industry analysis", default="")
    focus_points: List[str] = Field(description="Key areas to analyze", default=[])

class CombinedAnalysis(BaseModel):
    """Combined analysis from both agents"""
    overview: str = Field(description="Executive summary of combined analysis", default="")
    economic_analysis: Optional[EconomicData] = Field(description="Economic analysis results", default=None)
    industry_analysis: Optional[IndustryData] = Field(description="Industry analysis results", default=None)
    key_insights: List[str] = Field(description="Key insights from combined analysis", default=[])
    recommendations: List[str] = Field(description="Strategic recommendations", default=[])
    risks: List[str] = Field(description="Combined risk assessment", default=[])

@dataclass(kw_only=True)
class OrchestratorState:
    stock: str = field(default=None)
    plan: Optional[OrchestratorPlan] = field(default=None)
    final_economic_report: Annotated[List[str], operator.add] = field(default_factory=list)
    final_industry_report: Annotated[List[str], operator.add] = field(default_factory=list)
    final_quantitative_report: Annotated[List[str], operator.add] = field(default_factory=list)
    final_report: str = field(default="")

class OrchestratorInput(TypedDict):
    stock: str

class OrchestratorOutput(TypedDict):
    final_report: str
