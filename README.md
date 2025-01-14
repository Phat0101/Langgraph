# Stock Analysis Multi-Agent System

An AI-powered system using multiple specialized agents for comprehensive stock analysis through LangGraph.

## Project Overview

This system employs a coordinated multi-agent approach to analyze stocks:

### Orchestrator
- Coordinates analysis workflow between specialized agents
- Combines individual analyses into comprehensive reports
- Manages research planning and execution

### Specialized Agents
1. **Economic Analyst**
   - Analyzes macroeconomic conditions
   - Evaluates monetary and fiscal policies
   - Assesses economic risks and opportunities

2. **Industry Analyst**
   - Conducts industry research and competitive analysis
   - Evaluates market trends and dynamics
   - Analyzes regulatory environment

3. **Quantitative Analyst**
   - Performs financial metrics analysis
   - Evaluates company performance
   - Conducts valuation analysis

## Project Structure

```
langgraph/
├── .env                       # Environment variables
├── README.md                  # Project documentation
├── Orchestrator/             
│   ├── orchestrator.py        # Main coordination logic
│   ├── state.py              # Orchestrator state definitions
│   └── prompts.py            # Orchestrator system prompts
├── Economic_Analyst/
│   ├── economic_analyst.py    # Economic analysis workflow
│   ├── state.py              # Economic analyst state
│   └── prompts.py            # Economic analysis prompts
├── Industry_Analyst/     
│   ├── research_parallel.py   # Industry analysis workflow
│   ├── state.py              # Industry analyst state
│   └── prompts.py            # Industry analysis prompts
└── Quantitative_Analyst/
    ├── quantitative_analyst.py # Financial analysis workflow
    ├── state.py               # Quantitative analyst state
    └── prompts.py             # Financial analysis prompts
```

## Environment Setup

1. Clone the repository
2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```
3. Install dependencies:
```bash
pip install langchain langgraph tavily-python python-dotenv langchain-google-genai langsmith quickfs-python
```

## Required Environment Variables

Create a `.env` file with the following variables:

```properties
# AI Services
GOOGLE_GENERATIVE_AI_API_KEY=  # Gemini API key
TAVILY_API_KEY=                # Tavily search API key
QUICKFS_API_KEY=               # QuickFS API key for financial data

# LangSmith Configuration
LANGCHAIN_TRACING_V2=true
LANGCHAIN_ENDPOINT="https://api.smith.langchain.com"
LANGCHAIN_API_KEY=             # LangSmith API key
LANGCHAIN_PROJECT=             # Your project name
```

## Usage

```python
from Orchestrator.orchestrator import analyze_stock

async def main():
    result = await analyze_stock("AAPL")
    print(result["final_report"])
```

## Features

- **Multi-Agent Architecture**: Specialized agents for economic, industry, and quantitative analysis
- **Parallel Processing**: Concurrent analysis execution for efficiency
- **Source Deduplication**: Eliminates duplicate sources across all analyses
- **Iterative Analysis**: Agents use reflection for research refinement
- **Comprehensive Reporting**: Combines multiple expert analyses into cohesive reports

## License

MIT License

## Author

Patrick Nguyen

## Ideas from:
https://github.com/langchain-ai/report-mAIstro/tree/main
https://github.com/langchain-ai/research-rabbit/tree/main/src/research_rabbit
https://github.com/langchain-ai/data-enrichment/blob/main/src/enrichment_agent