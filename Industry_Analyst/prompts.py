RESEARCH_PLAN_PROMPT = """Create a comprehensive research plan for analyzing the {topic} industry. Focus on:
1. Industry structure and market dynamics
2. Competitive landscape and market shares
3. Growth drivers and market trends
4. Regulatory environment and barriers to entry
5. Technology and innovation impact"""

ANALYSIS_PROMPT = """Analyze this industry data:

{formatted_results}

Focus your analysis on:
1. Market structure and competitive dynamics
2. Industry growth trends and drivers
3. Key success factors and barriers to entry
4. Regulatory and technological environment
5. Future outlook and potential disruptions"""

SUMMARY_PROMPT = """Based on the existing summary and new findings, create or extend a comprehensive industry analysis.

Current Summary: {current_summary}
New Findings: {analysis}

Structure the analysis (~800 words) using these sections:

# Executive Summary
- Industry overview and significance
- Key findings and market dynamics
- Overall industry outlook

# Industry Structure & Classification
- Market definition and scope
- Value chain analysis
- Key industry segments
- Industry classification (GICS/NAICS)

# Competitive Analysis
- Market concentration and leadership
- Entry barriers and success factors
- Compare against the key players, their market shares and their strengths/weaknesses
- Competitive advantages and strategies

# Market Dynamics & Performance
- Market size and growth trends
- Demand drivers and growth catalysts
- Pricing dynamics and profitability
- Supply chain characteristics

# Operating Environment
- Regulatory framework and compliance
- Technological landscape and innovation
- Economic sensitivity and cycles
- ESG considerations

# Industry Trends & Disruption
- Emerging market trends
- Technological disruption
- Changing consumer preferences
- Innovation and R&D focus

# Risk Assessment
- Market-specific risks
- Operational challenges
- Regulatory threats
- Macroeconomic factors

# Future Outlook
- Growth projections and forecasts
- Strategic opportunities
- Potential challenges
- Industry transformation

Support each section with:
- Specific data points and metrics where available
- Recent market developments
- Competitive insights
- Forward-looking indicators

Back up the analysis with numers and statistics to provide a solid foundation for the insights only when available.
Focus on creating a clear narrative that integrates the new findings with existing knowledge."""

REFLECTION_PROMPT = """Reflect on the research using this search query:
{query}

Current Knowledge: {current_summary}

If more research is needed for the same query, propose a refined query and set the sufficient to False (Limit the query length maximum to 10 words). Otherwise, confirm the query is sufficient by setting it to True."""

COMBINE_SUMMARIES_PROMPT = """Synthesize these industry analyses into one comprehensive report:
Summaries: {summaries}

Combined_analysis: {combined_analysis}

Create a detailed industry analysis (~1200 words) for the {topic} industry using these sections:

# Executive Summary
- Industry overview and significance
- Key findings and market dynamics
- Overall industry outlook

# Industry Structure & Classification
- Market definition and scope
- Value chain analysis
- Key industry segments
- Industry classification (GICS/NAICS)

# Competitive Analysis
- Market concentration and leadership
- Entry barriers and success factors
- Compare against the key players, their market shares and their strengths/weaknesses
- Competitive advantages and strategies

# Market Dynamics & Performance
- Market size and growth trends
- Demand drivers and growth catalysts
- Pricing dynamics and profitability
- Supply chain characteristics

# Operating Environment
- Regulatory framework and compliance
- Technological landscape and innovation
- Economic sensitivity and cycles
- ESG considerations

# Industry Trends & Disruption
- Emerging market trends
- Technological disruption
- Changing consumer preferences
- Innovation and R&D focus

# Risk Assessment
- Market-specific risks
- Operational challenges
- Regulatory threats
- Macroeconomic factors

# Future Outlook
- Growth projections and forecasts
- Strategic opportunities
- Potential challenges
- Industry transformation

Support each section with:
- Specific data points and metrics
- Market statistics and trends
- Competitive insights
- Forward-looking indicators

Structure:
- Use ## for section title (Markdown format)
- Only use ONE structural element IF it helps clarify your point:
  * Either a focused table comparing few key items (using Markdown table syntax)
  * Or a short list (3-5 items) using proper Markdown list syntax:
    - Use `*` or `-` for unordered lists
    - Use `1.` for ordered lists
    - Ensure proper indentation and spacing
    
Best Practices and Industry Standards:
- Objectivity and Neutrality: Base your analysis on facts and evidence, avoiding personal biases.
- Data-Driven Analysis: Support your claims with quantifiable data, using reliable and reputable sources.
- Transparency: Clearly cite all data sources, assumptions, and methodologies.
- Clarity and Conciseness: Present information in a clear, organized, and easy-to-understand format.
- Forward-Looking Perspective: Consider future trends and their potential impact on the industry and the companies within it.
- Use of Industry Frameworks: Apply well-established frameworks like Porter's Five Forces, SWOT Analysis, and PESTLE analysis.
- Regular Updates: Update your analysis as new information becomes available.
- Avoidance of Conflicts of Interest: Disclose any potential conflicts of interest.


Back up the analysis with numers and statistics to provide a solid foundation for the insights only when available.
Focus on creating a cohesive narrative that demonstrates deep understanding of industry dynamics and future direction."""
