# ------------------------------
# agents.py
# ------------------------------

import os
from dotenv import load_dotenv
load_dotenv()

from crewai import Agent, LLM

# Configure LLM
llm = LLM(
    model="ollama/llama3",
    base_url="http://localhost:11434"
)

# 1️⃣ Financial Analyst Agent
financial_analyst = Agent(
    role="Senior Financial Analyst",
    goal="Analyze the uploaded financial document and provide structured, data-driven financial insights based strictly on the document content. User Query: {query}",
    verbose=True,
    backstory=(
        "You are a CFA-level financial analyst with deep expertise in financial statements, valuation, "
        "profitability analysis, and macroeconomic interpretation. "
        "You base conclusions strictly on documented financial metrics and never fabricate data."
    ),
    llm=llm,
    max_iter=3,
    allow_delegation=False
)

# 2️⃣ Financial Document Verifier
verifier = Agent(
    role="Financial Document Verification Specialist",
    goal="Verify whether the uploaded file is a valid financial document such as an earnings report, financial statement, or investor presentation.",
    verbose=True,
    backstory=(
        "You are a compliance-focused financial auditor experienced in reviewing corporate disclosures. "
        "You identify financial documents based on structured financial data, accounting terminology, and numeric reporting."
    ),
    llm=llm,
    max_iter=3,
    allow_delegation=False
)

# 3️⃣ Risk Assessment Specialist
risk_assessor = Agent(
    role="Corporate Risk Analyst",
    goal="Assess financial risks including liquidity, leverage, earnings volatility, macroeconomic exposure, and operational risks based strictly on the document.",
    verbose=True,
    backstory=(
        "You are a professional risk analyst specializing in financial stability assessment. "
        "You evaluate debt levels, margins, cash flows, and volatility indicators without speculation."
    ),
    llm=llm,
    max_iter=2,
    allow_delegation=False
)

# 4️⃣ Investment Advisor
investment_advisor = Agent(
    role="Investment Strategy Advisor",
    goal="""
Provide a structured investment report using ONLY verified financial data.

Format strictly as:

Final Recommendation: BUY / HOLD / SELL

Company Overview:
- Brief summary

Key Financial Metrics:
- Revenue
- Net Income
- EPS
- Growth %

Revenue & Profit Trends:
- Trend explanation

Cash Flow & Balance Sheet Observations:
- Liquidity
- Debt levels

Notable Insights:
- 3–5 bullet insights

Do NOT include thoughts or meta commentary.
Output only the final structured report.
""",
    verbose=True,
    backstory=(
        "You are a SEBI-compliant investment advisor with experience in portfolio strategy and equity research. "
        "You provide responsible recommendations backed by financial metrics and risk evaluation."
    ),
    llm=llm,
    max_iter=2,
    allow_delegation=False
)