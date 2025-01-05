RESEARCH_PLAN_PROMPT = """Create a research plan for analyzing the {topic} industry."""

ANALYSIS_PROMPT = """Analyze this data for {query}:\n{formatted_results}"""

SUMMARY_PROMPT = """Based on the existing summary and new findings, create or extend a comprehensive stock analysis.
    
Format the response in markdown with ~500 words total:

Current Summary: {current_summary}
New Findings: {analysis}

Please structure the analysis using these sections and bullet points:

# Market Position
- Current market share and positioning
- Key competitive advantages
- Brand strength and recognition

# Financial Performance
- Revenue trends and growth rates
- Profit margins and profitability metrics
- Cash flow and balance sheet highlights

# Growth Potential
- Market expansion opportunities
- New product/service developments
- Strategic partnerships or acquisitions

# Risk Assessment
- Market-specific risks
- Competitive threats
- Regulatory challenges

# Industry Trends
- Current market dynamics
- Emerging technologies impact
- Regulatory environment changes

# Investment Outlook
- Short-term price targets
- Long-term growth prospects
- Key metrics to monitor

Format each point as a concise bullet with supporting data when available.
Focus on facts over speculation and cite specific numbers where possible.
Leave out blank sections if data is not available."""

REFLECTION_PROMPT = """Reflect on the research using this search query:
{query}

Current Knowledge: {current_summary}

If more research is needed for the same query, propose a refined query and set the sufficient to False (Limit the query length maximum to 10 words). Otherwise, confirm the query is sufficient by setting it to True."""

COMBINE_SUMMARIES_PROMPT = """Combine these summaries into one coherent analysis:
{summaries} for the {topic}."""
