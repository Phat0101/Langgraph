from dataclasses import dataclass, field
from typing import List, Optional, Literal, Annotated, Dict, Union
from typing_extensions import TypedDict
from pydantic import BaseModel, Field
import operator
import datetime

today = datetime.date.today()

# Base Schema Definitions
class GlobalEconomics(BaseModel):
    """Global economic metrics"""
    gdp_growth: str = Field(description="Global GDP growth rates and trends", default="Unknown")
    inflation: str = Field(description="Global inflation rates and trends", default="Unknown")
    interest_rates: str = Field(description="Major central banks' interest rates", default="Unknown")
    exchange_rates: str = Field(description="Key exchange rate movements", default="Unknown")
    commodity_prices: str = Field(description="Trends in key commodity prices", default="Unknown")
    geopolitical_factors: str = Field(description="Major geopolitical risks and impacts", default="Unknown")

class DomesticEconomics(BaseModel):
    """Domestic economic metrics"""
    gdp_growth: str = Field(description="Domestic GDP growth and trends", default="Unknown")
    consumer_spending: str = Field(description="Consumer confidence and spending", default="Unknown")
    employment: str = Field(description="Employment and wage trends", default="Unknown")
    investment: str = Field(description="Business investment trends", default="Unknown")
    fiscal_policy: str = Field(description="Government fiscal policies", default="Unknown")
    monetary_policy: str = Field(description="Central bank policies", default="Unknown")
    housing_market: str = Field(description="Housing market trends", default="Unknown")

class IndustryEconomics(BaseModel):
    """Industry-specific economic impacts"""
    demand_elasticity: str = Field(description="Price and income elasticity", default="Unknown")
    input_cost_sensitivity: str = Field(description="Sensitivity to input costs", default="Unknown")
    pricing_power: str = Field(description="Industry pricing power", default="Unknown")
    interest_rate_sensitivity: str = Field(description="Interest rate impacts", default="Unknown")
    currency_sensitivity: str = Field(description="Exchange rate impacts", default="Unknown")
    government_support: str = Field(description="Government subsidies and incentives", default="Unknown")

class EconomicRiskItem(BaseModel):
    """Structure for economic risks"""
    title: str = Field(description="Title of the economic risk", default="No title")
    description: str = Field(description="Description of the economic risk", default="No description")
    severity: Literal["Low", "Medium", "High", "Critical"] = Field(description="Severity level of the risk", default="Medium")
    probability: Literal["Low", "Medium", "High"] = Field(description="Probability of occurrence", default="Medium")
    timeframe: str = Field(description="Expected timeframe for risk manifestation", default="Unknown")
    impact_areas: List[str] = Field(description="Areas of economic impact", default=["Unknown"])
    mitigation: str = Field(description="Potential mitigation strategies", default="No mitigation")
    indicators: List[str] = Field(description="Key indicators to monitor", default=["No indicators"])

class EconomicData(BaseModel):
    """Economic analysis data structure"""
    overview: str = Field(description="Executive summary of economic conditions", default="")
    global_economics: GlobalEconomics = Field(description="Global economic metrics", default=GlobalEconomics())
    domestic_economics: DomesticEconomics = Field(description="Domestic economic metrics", default=DomesticEconomics())
    industry_economics: IndustryEconomics = Field(description="Industry economic impacts", default=IndustryEconomics())
    risks: List[EconomicRiskItem] = Field(description="Economic risks", default=[])
    opportunities: List[str] = Field(description="Economic opportunities", default=[])
    scenarios: str = Field(description="Economic scenarios", default="")
    recommendations: str = Field(description="Investment implications", default="")

class ResearchPlan(BaseModel):
    """Research planning structure"""
    focus_areas: List[str] = Field(description="Key areas to research")
    search_queries: List[str] = Field(
        description=f"""Create 3 Search queries for {today} covering:
        - Global economic indicators (GDP, inflation, interest rates)
        - Domestic economic conditions and policies
        - Industry-specific economic impacts and sensitivities
        - Macroeconomic risks and opportunities
        - Economic forecasts and future outlook"""
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
    final_economic_report: Annotated[List[str], operator.add] = field(default_factory=list)
    completed_analyses: Annotated[List[EconomicData], operator.add] = field(default_factory=list)

@dataclass(kw_only=True)
class ResearchStateInput(TypedDict):
    topic: str = field(default=None)

@dataclass(kw_only=True)
class ResearchStateOutput(TypedDict):
    final_economic_report: Annotated[List[str], operator.add] = field(default_factory=list)
    completed_analyses: Annotated[List[EconomicData], operator.add] = field(default_factory=list)

@dataclass(kw_only=True)
class AnalystState:
    search_query: str = field(default=None)
    research_loop_count: int = field(default=0)
    running_summaries: Annotated[List[str], operator.add] = field(default_factory=list)
    web_research_results: Annotated[list, operator.add] = field(default_factory=list)
    sources_gathered: Annotated[List[str], operator.add] = field(default_factory=list)
    analyses: Annotated[List[EconomicData], operator.add] = field(default_factory=list)

@dataclass(kw_only=True)
class AnalystOutputState(TypedDict):
    completed_analyses: Annotated[List[EconomicData], operator.add] = field(default_factory=list)
    sources_gathered: Annotated[List[str], operator.add] = field(default_factory=list)
    running_summaries: Annotated[List[str], operator.add] = field(default_factory=list)

