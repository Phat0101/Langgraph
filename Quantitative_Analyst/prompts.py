SYMBOL_REFLECTION_PROMPT = """Given the failed attempt to fetch financial data for the stock {stock} using symbol {symbol}, 
suggest an alternative symbol format to try. Consider these formats:
1. US stocks: AAPL:US, AAPL.US, AAPL
2. Australian stocks: CBA:AU, CBA.AX
3. Other formats: {stock}.L (London), {stock}.TO (Toronto)

Current attempt count: {attempt_count}
Previous attempts: {previous_attempts}

Determine if we should:
1. Try a different symbol format
2. Consider the other exchange or market of the stock
3. Stop trying if we've exhausted likely formats"""

FINANCIAL_ANALYSIS_PROMPT = '''Analyze the financial data for {stock}:

# DATA
{formatted_data}

Perform a comprehensive quantitative analysis (1200 words) focusing on:

1. Profitability Analysis
- Gross margin trends
- Operating margins
- Net profit margins
- Return metrics (ROE, ROA, ROIC)
- Earnings quality

2. Liquidity & Solvency
- Working capital management
- Cash conversion cycle
- Debt coverage ratios
- Interest coverage
- Capital structure analysis

3. Growth & Efficiency
- Revenue growth trends
- Earnings growth sustainability
- Cash flow growth
- Asset turnover
- Capital efficiency

4. Valuation Metrics
- Current multiples (P/E, P/B, EV/EBITDA)
- Historical valuation trends
- Industry comparison
- DCF implications

5. Cash Flow Analysis
- Operating cash flow trends
- Free cash flow generation
- Cash flow quality
- Working capital requirements

6. Risk Assessment
- Financial leverage
- Operating leverage
- Earnings volatility
- Cash flow stability
- Credit metrics

7. Capital Allocation
- Dividend policy
- Share repurchases
- CAPEX trends
- R&D investment
- M&A activity

Provide quantitative evidence and specific metrics for each point.
Flag any significant deviations or concerning trends.


'''

# Each metric should be formatted as:
# {{
#     "value": "number",
#     "unit": "%" or "ratio" or "$M",
#     "trend": "increasing" or "decreasing" or "stable",
#     "conclusion": "Conclusion or interpretation of the metric"
# }}

# Required metrics format:
# {{
#     "profitability": {{
#         "gross_margin": {{
#             "value": "45.2",
#             "unit": "%",
#             "trend": "increasing",
#             "conclusion: "Gross margin has improved due to cost efficiencies"
#         }},
#         "operating_margin": {{
#             "value": "25.3",
#             "unit": "%",
#             "trend": "stable",
#             "conlusion": "Operating margin has remained consistent over the period"
#         }}
#     }},
#     "liquidity": {{
#         "current_ratio": {{
#             "value": "2.1",
#             "unit": "ratio",
#             "trend": "stable",
#             "conlusion": "Current ratio indicates sufficient liquidity"
#         }}
#     }}
# }}