from dataclasses import dataclass, field
from typing import List, Optional, Literal, Annotated, Dict
from typing_extensions import TypedDict
from pydantic import BaseModel, Field
import operator
import datetime

today = datetime.date.today()

# Base Schema Definitions
class NewsItem(BaseModel):
    """Structure for news items"""
    title: str = Field(description="Title of the news article", default="No title")
    content: str = Field(description="Content of the news article", default="No content")
    source: str = Field(description="Source of the news", default="No source")
    date: str = Field(description="Publication date", default="No date")

class ProjectionItem(BaseModel):
    """Structure for industry projections"""
    description: str = Field(description="Details of the projection", default="No description")
    timeframe: str = Field(description="Timeframe for the projection", default="No timeframe")
    likelihood: str = Field(description="Likelihood of the projection", default="No likelihood")

class RiskItem(BaseModel):
    """Structure for industry risks"""
    title: str = Field(description="Title of the risk", default="No title")
    description: str = Field(description="Description of the risk", default="No description")
    severity: str = Field(description="Severity level of the risk", default="No severity")
    mitigation: str = Field(description="Potential mitigation strategies", default="No mitigation")

class CompetitorItem(BaseModel):
    """Structure for competitor analysis"""
    name: str = Field(description="Name of the competitor", default="No name")
    description: str = Field(description="Description of the competitor", default="No description")
    strengths: List[str] = Field(description="Key strengths", default=["No strengths"])
    weaknesses: List[str] = Field(description="Key weaknesses", default=["No weaknesses"])

class IndustryData(BaseModel):
    """Industry research data structure"""
    news: List[NewsItem] = Field(description="Latest industry news", default=[])
    projections: List[ProjectionItem] = Field(description="Future industry projections", default=[])
    risks: List[RiskItem] = Field(description="Industry risks", default=[])
    competitors: List[CompetitorItem] = Field(description="Key competitors", default=[])

class ResearchPlan(BaseModel):
    """Research planning structure"""
    focus_areas: List[str] = Field(description="Key areas to research")
    search_queries: List[str] = Field(description=f"3 Search queries for data gathering including news, projections, risks, and competitors for {today}")
    analysis_points: List[str] = Field(description="Points to analyze")
    
class Reflection(BaseModel):
    """Reflection structure"""
    sufficient: bool = Field(description="Indicates if the current research is sufficient", default=False)
    refined_query: str = Field(description="Refined search query", default="")

@dataclass(kw_only=True)
class ResearchState:
    topic: str = field(default=None)
    plan: Optional[ResearchPlan] = field(default=None)
    search_query: str = field(default=None)
    search_queries: List[str] = field(default_factory=list)
    web_research_results: Annotated[list, operator.add] = field(default_factory=list)
    sources_gathered: Annotated[List[str], operator.add] = field(default_factory=list)
    research_loop_count: int = field(default=0)
    running_summaries: Annotated[List[str], operator.add] = field(default_factory=list)
    final_report: str = field(default=None)
    completed_analyses: Annotated[List[IndustryData], operator.add] = field(default_factory=list)

@dataclass(kw_only=True)
class ResearchStateInput(TypedDict):
    topic: str = field(default=None)

@dataclass(kw_only=True)
class ResearchStateOutput(TypedDict):
    final_report: str = field(default=None)

@dataclass(kw_only=True)
class AnalystState:
    search_query: str = field(default=None)
    research_loop_count: int = field(default=0)
    running_summaries: Annotated[List[str], operator.add] = field(default_factory=list)
    web_research_results: Annotated[list, operator.add] = field(default_factory=list)
    sources_gathered: Annotated[List[str], operator.add] = field(default_factory=list)
    analyses: Annotated[List[IndustryData], operator.add] = field(default_factory=list)

@dataclass(kw_only=True)
class AnalystOutputState(TypedDict):
    completed_analyses: Annotated[List[IndustryData], operator.add] = field(default_factory=list)
    sources_gathered: Annotated[List[str], operator.add] = field(default_factory=list)
    running_summaries: Annotated[List[str], operator.add] = field(default_factory=list)
