# AI Multi-Agent Financial Document Analyzer

### Debug Challenge Submission – Generative AI Internship

---

## Overview

This project is a fully debugged and optimized multi-agent financial document analysis system built using CrewAI and FastAPI.

I analyzed the issues in the existing codebase, identified deterministic failures and prompt inefficiencies, and restructured the system to ensure stable and predictable execution.

The final system is capable of:

* Verifying financial documents
* Performing structured financial analysis
* Assessing financial risks
* Providing a final investment recommendation (BUY / HOLD / SELL)
* Processing requests in the background
* Persisting results in a database

The system runs end-to-end successfully using a local LLM setup (Ollama + Llama3).

---

## Python Version

Python 3.11.9

---

## Technology Stack

* FastAPI (Backend API)
* CrewAI (Multi-agent orchestration)
* Ollama (Local LLM runtime)
* Llama3 model
* SQLite (Persistent storage)
* LangChain PyPDFLoader (PDF extraction)
* Uvicorn (ASGI server)

---

## System Architecture

The system follows a structured multi-agent execution pipeline:

User Upload (PDF)
→ FastAPI Endpoint
→ Background Task Execution
→ PDF Text Extraction
→ CrewAI Sequential Agents
→ Database Storage
→ Retrieval via API

### Agent Flow

1. Financial Document Verification Specialist
2. Senior Financial Analyst
3. Corporate Risk Analyst
4. Investment Strategy Advisor

Execution is strictly sequential using `Process.sequential`, with explicit task dependency linking to ensure deterministic behavior and proper context propagation.

---

## Deterministic Bugs Identified & Fixed

### 1. Missing Document Text Injection

The original flow did not correctly pass extracted document content to the agents.

**Fix:**
Implemented PDF extraction using `PyPDFLoader` and passed trimmed `document_text` directly into the Crew kickoff payload.

---

### 2. Blocking Execution Model

The agent workflow was executed synchronously, blocking API responses.

**Fix:**
Converted execution to FastAPI `BackgroundTasks`, enabling non-blocking request handling and allowing concurrent request processing.

---

### 3. No Database Persistence

Analysis results were not stored persistently.

**Fix:**
Integrated SQLite database (`analysis.db`) with automatic initialization during application startup and structured result storage.

---

### 4. Uncontrolled Token Usage

Large financial PDFs caused unstable LLM behavior and excessive token consumption.

**Fix:**
Implemented controlled trimming of document text to 8000 characters before passing it to the LLM to ensure stable CPU inference using Ollama.

---

### 5. Improper Task Dependency Flow

Risk and investment tasks were not fully context-aware.

**Fix:**
Explicitly linked task contexts:

* Risk assessment depends on financial analysis
* Investment recommendation depends on both financial analysis and risk assessment

This ensures logical sequencing and consistent reasoning flow.

---

### 6. Weak Output Structure

Agents produced inconsistent outputs and occasional meta commentary.

**Fix:**
Rewrote agent goals with strict structured output enforcement, including:

* Clearly defined report sections
* Explicit formatting rules
* “Do NOT include thoughts or meta commentary” constraints
* Controlled iteration limits
* Delegation disabled to maintain predictable execution

---

## Prompt Optimization Improvements

Original prompts were loosely defined and allowed unnecessary meta reasoning.

Improvements performed:

* Enforced structured section headers
* Restricted output formatting explicitly
* Added financial terminology constraints
* Controlled reasoning verbosity using `max_iter`
* Disabled delegation to prevent uncontrolled agent chaining

These changes ensured consistent, professional-grade financial reports.

---

## Custom CrewAI Tool Implementation

A reusable PDF ingestion tool was implemented using CrewAI’s `@tool` decorator:

```python
@tool
def read_data_tool(path: str) -> str:
```

### Features:

* Validates file path type
* Verifies file existence
* Extracts structured PDF content using `PyPDFLoader`
* Cleans excessive newline characters
* Applies 8000-character safety limit

This ensures safe and deterministic document ingestion before multi-agent processing.

---

## API Endpoints

### GET /

Health check endpoint.

Response:

```json
{
  "message": "Financial Document Analyzer API is running"
}
```

---

### POST /analyze

Uploads a financial PDF for background analysis.

Request:

* Multipart form-data
* `file` (PDF)
* `query` (optional)

Response:

```json
{
  "status": "processing",
  "message": "Analysis started in background. Check /analyses endpoint for results."
}
```

Processing runs asynchronously in the background.

---

### GET /analyses

Returns all stored analysis results from the SQLite database.

Response:

```json
{
  "analyses": [...]
}
```

---

## Database Schema

Database: `analysis.db`
Table: `analyses`

Columns:

* `id` (Primary Key)
* `filename`
* `query`
* `result`

The database is initialized automatically when the application starts.

---

## Setup Instructions

### 1. Clone Repository

```bash
git clone <your_repo_link>
cd financial-document-analyzer
```

---

### 2. Create Virtual Environment

```bash
python -m venv venv
```

Windows:

```bash
venv\Scripts\activate
```

---

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Install and Run Ollama

Download Ollama from:
[https://ollama.com](https://ollama.com)

Pull and run Llama3:

```bash
ollama pull llama3
ollama run llama3
```

Ensure Ollama is running at:

```
http://localhost:11434
```

---

### 5. Run API Server

```bash
uvicorn main:app --reload
```

Access Swagger UI at:

```
http://127.0.0.1:8000/docs
```

---

## Repository Hygiene

To maintain a clean and production-ready repository, the following files and directories are excluded using `.gitignore`:

* `venv/`
* `__pycache__/`
* `analysis.db`
* `data/`
* `.env`
* `*.pyc`

This prevents local artifacts and sensitive files from being committed.

---

## Bonus Implementations

* Background processing model for concurrent request handling
* SQLite database integration
* Structured task dependency management
* Custom CrewAI tool for document ingestion
* Controlled LLM token usage
* Modular, production-ready architecture

---

## Production Considerations

* Designed for local LLM inference using Ollama
* Modular agent architecture enables easy scaling
* Can be upgraded to Redis/Celery for distributed queue management
* Clear separation of concerns across agents and tasks
* Deterministic execution model

---

## Final Status

The system runs end-to-end successfully:

* Upload financial PDF
* Automatic background processing
* Multi-agent structured financial analysis
* Risk evaluation
* Final investment recommendation
* Persistent database storage
* Retrieval via API endpoint

All major deterministic bugs and inefficient prompts have been resolved.

---

