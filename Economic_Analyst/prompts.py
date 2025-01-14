RESEARCH_PLAN_PROMPT = """Create a comprehensive research plan for analyzing the economic impacting {topic} . Focus on:
1. Global economic indicators (GDP, inflation, interest rates)
2. Domestic economic conditions and policies
3. Industry-specific economic impacts and sensitivities
4. Macroeconomic risks and opportunities
5. Economic forecasts and future outlook"""


REFLECTION_PROMPT = """Reflect on the research using this search query:
{query}

Current Knowledge: {current_summary}

If more research is needed for the same query, propose a refined query and set the sufficient to False (Limit the query length maximum to 10 words). Otherwise, confirm the query is sufficient by setting it to True."""

ANALYSIS_PROMPT = """Analyze the economic environment:

{formatted_results}

Structure your analysis following these sections:

I. Executive Summary
- Brief overview of current macroeconomic environment
- Key findings (2-3 bullet points)
- Overall outlook and implications

II. Global Economic Environment
- GDP growth trends and forecasts
- Inflation analysis
- Interest rates impact
- Exchange rates
- Geopolitical factors
- Commodity prices

III. Domestic Economic Environment
- GDP growth and trends
- Consumer spending patterns
- Employment and wages
- Investment trends
- Fiscal and monetary policy
- Housing market impact

IV. Industry-Specific Economic Impacts
- Demand elasticity analysis
- Input cost sensitivity
- Pricing power assessment
- Interest rate sensitivity
- Currency exposure
- Government support measures

V. Risks and Opportunities
- Key macroeconomic risks
- Economic opportunities
- Scenario analysis

VI. Investment Implications
- Impact on valuation
- Investment thesis
- Recommendations"""

SUMMARY_PROMPT = """Based on the existing analysis and new findings, create a comprehensive economic assessment.

Current Analysis: {current_summary}
New Findings: {analysis}

Structure the analysis (~800 words) using these sections:

# Executive Summary
- Brief overview of macroeconomic environment and impact
- Key findings (2-3 bullet points on critical economic factors)
- Overall economic outlook (positive/negative/neutral) and implications

# Global Economic Environment
## GDP Growth
- Current growth rates and historical trends
- Future growth forecasts
- Regional variations and imbalances

## Inflation
- Current rates and historical trends
- Analysis of inflation drivers
- Impact on spending and costs
- Central bank responses

## Interest Rates
- Current levels and central bank policies
- Expected future changes
- Impact on borrowing and investment

## Exchange Rates
- Current movements and volatility
- Impact on competitiveness

## Geopolitical Factors
- Political risks and trade tensions
- Supply chain impacts

## Commodity Prices
- Key commodity trends
- Impact on industry costs

# Domestic Economic Environment
## GDP Growth
- Domestic growth rates and trends
- Future market forecasts
- Growth components analysis

## Consumer Activity
- Spending patterns and confidence
- Income and employment effects

## Employment
- Unemployment trends
- Labor market conditions
- Wage growth impact

## Investment Climate
- Business investment trends
- Policy impacts

## Government Policy
- Fiscal policy analysis
- Monetary policy measures
- Housing market conditions

# Industry-Specific Economic Impacts
## Demand Analysis
- Price and income elasticity
- Economic cycle sensitivity

## Cost Structure
- Input cost sensitivity
- Supply chain impacts

## Market Power
- Pricing power assessment
- Competitive factors

## Financial Sensitivity
- Interest rate exposure
- Currency impacts
- Government support

# Economic Risks and Opportunities
- Key macroeconomic risks
- Growth opportunities
- Scenario analysis

# Investment Implications
- Economic factor summary
- Valuation impacts
- Investment thesis
- Key catalysts and risks
- Recommendations

Support each section with:
- Specific data points and metrics
- Recent economic developments
- Forward-looking indicators
- Quantitative analysis where available

Focus on creating a clear narrative that demonstrates understanding of economic dynamics and their specific impacts."""

COMBINE_SUMMARIES_PROMPT = """Synthesize these economic analyses into a comprehensive report:

Summaries: {summaries}

Combined analyses: {combined_analysis}

Create a detailed economic assessment (~1200 words) for {topic} using these sections:

# Executive Summary
## Overview
- Current macroeconomic environment
- Impact on {topic}
- Critical economic factors

## Key Findings and Outlook
- Major economic impacts
- General outlook and implications

# Global Economic Environment
## Growth and Monetary Conditions
- GDP trends and forecasts
- Inflation dynamics
- Interest rate environment
- Exchange rate impacts

## External Factors
- Geopolitical considerations
- Trade conditions
- Commodity markets

# Domestic Economic Environment
## Economic Growth
- GDP components
- Market forecasts
- Structural factors

## Market Conditions
- Consumer dynamics
- Employment trends
- Investment climate
- Policy environment

# Industry-Specific Impacts
## Demand and Supply
- Economic sensitivity
- Cost structure impacts
- Market power analysis

## Financial Effects
- Interest rate exposure
- Currency sensitivity
- Government intervention

# Risk-Opportunity Assessment
## Risk Analysis
- Macroeconomic threats
- Probability assessment
- Impact scenarios

## Opportunity Landscape
- Growth catalysts
- Market possibilities
- Scenario outcomes

# Investment Conclusions
## Economic Impact Summary
- Key factor analysis
- Valuation effects
- Investment case

## Investment Recommendations
- Investment thesis
- Risk factors
- Catalysts for growth

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
Create a cohesive narrative showing deep understanding of economic impacts on {topic}."""
