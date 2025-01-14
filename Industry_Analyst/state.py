from dataclasses import dataclass, field
from typing import List, Optional, Literal, Annotated, Dict, Union
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

class IndustryMetrics(BaseModel):
    """Industry performance metrics"""
    market_size: str = Field(description="Total market size", default="Unknown")
    growth_rate: str = Field(description="Industry growth rate", default="Unknown")
    profit_margins: str = Field(description="Average industry margins", default="Unknown")
    market_concentration: str = Field(description="Market concentration ratio", default="Unknown")

class PorterForce(BaseModel):
    """Structure for Porter's Five Forces analysis"""
    force: str = Field(description="Name of the force", default="No force")
    strength: Literal["Low", "Medium", "High", "Unknown"] = Field(description="Strength of the force", default="Unknown")
    description: str = Field(description="Detailed analysis", default="No description")
    key_factors: List[str] = Field(description="Key contributing factors", default=["No factors"])

class MarketTrend(BaseModel):
    """Structure for industry trends"""
    name: str = Field(description="Name of the trend", default="No name")
    impact: Literal["Positive", "Negative", "Neutral", "Unknown"] = Field(description="Impact on industry", default="Unknown")
    description: str = Field(description="Trend description", default="No description")
    timeframe: str = Field(description="Expected timeframe", default="No timeframe")

class IndustryData(BaseModel):
    """Industry research data structure"""
    overview: str = Field(description="Executive summary of the industry", default="")
    classification: str = Field(description="Industry classification codes (GICS/NAICS)", default="")
    metrics: IndustryMetrics = Field(description="Key industry metrics", default=IndustryMetrics())
    porters_forces: List[PorterForce] = Field(description="Porter's Five Forces analysis", default=[])
    trends: List[MarketTrend] = Field(description="Industry trends", default=[])
    news: List[NewsItem] = Field(description="Latest industry news", default=[])
    projections: List[ProjectionItem] = Field(description="Future industry projections", default=[])
    risks: List[RiskItem] = Field(description="Industry risks", default=[])
    competitors: List[CompetitorItem] = Field(description="Key competitors", default=[])

class ResearchPlan(BaseModel):
    """Research planning structure"""
    focus_areas: List[str] = Field(description="Key areas to research")
    search_queries: List[str] = Field(
        description=f"""Create 3 search queries for {today} covering:
        - Industry structure, market size, and dynamics
        - Competitive landscape and market shares
        - Growth drivers and market trends
        - Value chain and supply chain analysis
        - Regulatory environment and compliance
        - Technology trends and innovation
        - Market risks and challenges
        - ESG factors and sustainability
        - Future outlook and forecasts"""
    )
    analysis_points: List[str] = Field(description="Points to analyze")

class Reflection(BaseModel):
    """Reflection structure"""
    sufficient: bool = Field(description="Indicates if the current research is sufficient", default=False)
    refined_query: str = Field(description="Refined search query", default="")

@dataclass(kw_only=True)
class ResearchState:
    topic: str = field(default=None)
    plan: Optional[ResearchPlan] = field(default=None)
    search_queries: List[str] = field(default_factory=list)
    web_research_results: Annotated[list, operator.add] = field(default_factory=list)
    sources_gathered: Annotated[List[str], operator.add] = field(default_factory=list)
    running_summaries: Annotated[List[str], operator.add] = field(default_factory=list)
    final_industry_report: Annotated[List[str], operator.add] = field(default_factory=list)
    completed_analyses: Annotated[List[IndustryData], operator.add] = field(default_factory=list)

@dataclass(kw_only=True)
class ResearchStateInput(TypedDict):
    topic: str = field(default=None)

@dataclass(kw_only=True)
class ResearchStateOutput(TypedDict):
    # final_report: str = field(default=None)
    final_industry_report: Annotated[List[str], operator.add] = field(default_factory=list)
    completed_analyses: Annotated[List[IndustryData], operator.add] = field(default_factory=list)

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
