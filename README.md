# Industry Analysis AI Agents System

An AI-powered system for conducting comprehensive industry analysis using LangGraph

## Project Overview

This system performs automated industry research and analysis by:
- Creating research plans with targeted search queries
- Conducting parallel web searches using Tavily API
- Analyzing industry data, risks, and trends
- Generating comprehensive research reports

## Project Structure

```
langgraph/
├── .env                  # Environment variables
├── README.md             # Project overview
├── langgraph.json     # Langgraph configuration
├── Industry_Analyst/     
│   ├── research_parallel.py     # Main analysis workflow
│   ├── state.py                 # State definitions
│   └── prompts.py              # System prompts
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
pip install langchain langgraph tavily-python python-dotenv langchain-google-genai langsmith
```

## Required Environment Variables

Create a `.env` file with the following variables:

```properties
# AI Services
GOOGLE_GENERATIVE_AI_API_KEY=  # Gemini API key
TAVILY_API_KEY=                # Tavily search API key

# LangSmith Configuration
LANGCHAIN_TRACING_V2=true
LANGCHAIN_ENDPOINT="https://api.smith.langchain.com"
LANGCHAIN_API_KEY=             # LangSmith API key
LANGCHAIN_PROJECT=             # Your project name
```

## Usage

```python
from Industry_Analyst.research_parallel import analyze_industry

async def main():
    result = await analyze_industry("Research Palantir Stock Industry")
    print(result["final_report"])

```
Or use Langgraph Studio to run the analysis


## Features

- **Parallel Research**: Conducts multiple research queries simultaneously
- **Source Deduplication**: Eliminates duplicate sources and content
- **Iterative Analysis**: Refines research based on initial findings, reAct agents with reflection
- **Comprehensive Reporting**: Combines multiple analyses into coherent reports

## License

MIT License

## Author

Patrick Nguyen

## Ideas from:
https://github.com/langchain-ai/report-mAIstro/tree/main
https://github.com/langchain-ai/research-rabbit/tree/main/src/research_rabbit
https://github.com/langchain-ai/data-enrichment/blob/main/src/enrichment_agent

