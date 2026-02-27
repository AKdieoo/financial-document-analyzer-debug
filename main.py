from fastapi import FastAPI, File, UploadFile, Form, HTTPException, BackgroundTasks
import os
import uuid

from crewai import Crew, Process
from langchain_community.document_loaders import PyPDFLoader

from agents import (
    financial_analyst,
    verifier,
    investment_advisor,
    risk_assessor
)

from task import (
    verification,
    analyze_financial_document,
    risk_assessment,
    investment_analysis
)

from database import init_db, save_analysis

app = FastAPI(
    title="AI Multi-Agent Financial Document Analyzer",
    description="Multi-agent system with DB + background processing",
    version="2.0.0"
)

# ------------------------------
# Initialize DB on Startup
# ------------------------------

@app.on_event("startup")
def startup_event():
    init_db()


# ------------------------------
# Initialize Crew Once
# ------------------------------

financial_crew = Crew(
    agents=[
        verifier,
        financial_analyst,
        risk_assessor,
        investment_advisor
    ],
    tasks=[
        verification,
        analyze_financial_document,
        risk_assessment,
        investment_analysis
    ],
    process=Process.sequential,
    verbose=True
)


# ------------------------------
# Background Processing Function
# ------------------------------

def process_document(file_path, file_name, query):
    try:
        loader = PyPDFLoader(file_path)
        docs = loader.load()

        full_text = ""
        for d in docs:
            full_text += d.page_content + "\n"

        MAX_CHARS = 8000   # safe limit for Ollama CPU

        trimmed_text = full_text[:MAX_CHARS]

        response = financial_crew.kickoff({
            "query": query,
            "document_text": trimmed_text
        })

        save_analysis(file_name, query, response)

    finally:
        if os.path.exists(file_path):
            os.remove(file_path)


# ------------------------------
# Routes
# ------------------------------

@app.get("/")
async def root():
    return {"message": "Financial Document Analyzer API is running"}


@app.post("/analyze")
async def analyze_financial_document_api(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    query: str = Form(default="Analyze this financial document for investment insights")
):
    if not file or not file.filename:
        raise HTTPException(status_code=400, detail="No file uploaded.")

    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF documents supported.")

    file_id = str(uuid.uuid4())
    file_path = f"data/financial_document_{file_id}.pdf"

    os.makedirs("data", exist_ok=True)

    content = await file.read()

    with open(file_path, "wb") as f:
        f.write(content)

    if not query or query.strip() == "":
        query = "Analyze this financial document for investment insights"

    background_tasks.add_task(
        process_document,
        file_path,
        file.filename,
        query.strip()
    )

    return {
        "status": "processing",
        "message": "Analysis started in background. Check /analyses endpoint for results."
    }


@app.get("/analyses")
def get_analyses():
    import sqlite3
    conn = sqlite3.connect("analysis.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM analyses")
    rows = cursor.fetchall()
    conn.close()
    return {"analyses": rows}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)