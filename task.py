# ------------------------------
# task.py
# ------------------------------


from crewai import Task
from agents import (
    financial_analyst,
    verifier,
    investment_advisor,
    risk_assessor
)

# 1️⃣ Verification Task
verification = Task(
    description=(
        "Here is the financial document content:\n\n"
        "{document_text}\n\n"
        "Determine whether this is a valid financial document "
        "(earnings report, annual report, financial statement, investor presentation).\n\n"
        "If NOT financial, clearly reject it with reason.\n"
        "If valid, justify using financial terminology and structure."
    ),
    expected_output=(
        "VALID FINANCIAL DOCUMENT or NOT A FINANCIAL DOCUMENT\n"
        "Followed by 2-4 bullet points of justification."
    ),
    agent=verifier,
    async_execution=False,
)

# 2️⃣ Financial Analysis Task
analyze_financial_document = Task(
    description=(
        "Based strictly on the following financial document content:\n\n"
        "{document_text}\n\n"
        "User Query: {query}\n\n"
        "Provide a structured financial report including:\n"
        "1. Company Overview\n"
        "2. Key Financial Metrics\n"
        "3. Revenue & Profit Trends\n"
        "4. Cash Flow & Balance Sheet Observations\n"
        "5. Notable Insights\n\n"
        "Use ONLY information explicitly available in the document."
    ),
    expected_output=(
        "A structured financial report with clear section headers and bullet points."
    ),
    agent=financial_analyst,
    async_execution=False,
)

# 3️⃣ Risk Assessment Task
risk_assessment = Task(
    description=(
        "Using the financial analysis as context, assess:\n"
        "- Liquidity Risk\n"
        "- Leverage Risk\n"
        "- Earnings Volatility\n"
        "- Macroeconomic Exposure\n"
        "- Operational Risks\n\n"
        "Base conclusions strictly on documented financial metrics."
    ),
    expected_output=(
        "Structured risk report with clear headings and concise explanations."
    ),
    agent=risk_assessor,
    async_execution=False,
)

# 4️⃣ Investment Recommendation Task
investment_analysis = Task(
    description=(
        "Based on financial analysis and risk assessment, provide final recommendation:\n"
        "- BUY, HOLD, or SELL\n\n"
        "Justify using financial metrics and risk considerations."
    ),
    expected_output=(
        "Final Recommendation: BUY / HOLD / SELL\n"
        "Followed by concise justification."
    ),
    agent=investment_advisor,
    async_execution=False,
)

# -----------------------------
# 🔗 Task Dependency Linking
# -----------------------------

risk_assessment.context = [analyze_financial_document]

investment_analysis.context = [
    analyze_financial_document,
    risk_assessment
]