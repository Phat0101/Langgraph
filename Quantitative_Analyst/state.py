from dataclasses import dataclass, field
from typing import List, Optional, Dict, TypedDict, Annotated, Any
from pydantic import BaseModel, Field
import operator

class Reflection(BaseModel):
    """Reflection structure"""
    sufficient: bool = Field(description="Indicates if the data fetch was successful", default=False)
    refined_symbol: str = Field(description="Refined stock symbol to try", default="")
    attempt_count: int = Field(description="Number of attempts made", default=0)

class ResearchPlan(BaseModel):
    """Stock name query"""
    stock: str = Field(description="""Stock symbol to research, consider the following formats:
                      1. (Example) US stocks: AAPL:US, AAPL.US, AAPL
                      2. (Example) Australian stocks: CBA:AU, CBA.AX
                      3. Other formats: stockName:L (London), stockName:TO (Toronto)
                      """, default="")
    
@dataclass(kw_only=True)
class QuantAnalystState:
    stock: str = field(default=None)
    symbol_attempts: List[str] = field(default_factory=list)
    financial_data: str = field(default=None)
    research_loop_count: int = field(default=0)
    final_quantitative_report: Annotated[List[str], operator.add] = field(default_factory=list)

class QuantAnalystInput(TypedDict):
    stock: str

class QuantAnalystOutput(TypedDict):
    final_quantitative_report: Annotated[List[str], operator.add] = field(default_factory=list)
