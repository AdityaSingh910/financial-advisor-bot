"""
FastAPI Backend for the RAG-based Financial Advisory Assistant.
Provides the REST API endpoints for the frontend chat interface.
"""

import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from agents.orchestrator import run_pipeline


# Load environment variables
load_dotenv()

app = FastAPI(
    title="Financial Advisory AI",
    description="RAG-based Financial Advisory Assistant with Agentic AI",
    version="1.0.0",
)

# CORS — allow frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Request / Response Models ────────────────────────────────

class ChatRequest(BaseModel):
    query: str


class ChatResponse(BaseModel):
    success: bool
    query: str | None = None
    response: str | None = None
    risk_analysis: str | None = None
    sources: list[str] | None = None
    chunks_retrieved: int | None = None
    agent_trace: list[dict] | None = None
    total_duration_ms: int | None = None
    error: str | None = None


# ── Endpoints ────────────────────────────────────────────────

@app.get("/api/health")
def health_check():
    """Health check endpoint."""
    api_key = os.getenv("GROQ_API_KEY", "")
    has_key = bool(api_key and api_key != "your_groq_api_key_here")
    
    vector_store_exists = os.path.exists(
        os.path.join(os.path.dirname(__file__), "vector_store", "index.faiss")
    )
    
    return {
        "status": "healthy",
        "api_key_configured": has_key,
        "vector_store_ready": vector_store_exists,
    }


@app.post("/api/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    """
    Main chat endpoint.
    Takes a user query and runs it through the 3-agent pipeline.
    """
    if not request.query or not request.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")
    
    api_key = os.getenv("GROQ_API_KEY", "")
    if not api_key or api_key == "your_groq_api_key_here":
        raise HTTPException(
            status_code=500,
            detail="Groq API key not configured. Please set GROQ_API_KEY in backend/.env"
        )
    
    # Check vector store exists
    vector_store_path = os.path.join(os.path.dirname(__file__), "vector_store", "index.faiss")
    if not os.path.exists(vector_store_path):
        raise HTTPException(
            status_code=500,
            detail="Vector store not found. Please run 'python ingest.py' first."
        )
    
    try:
        result = run_pipeline(query=request.query.strip(), api_key=api_key)
        return ChatResponse(**result)
    except Exception as e:
        return ChatResponse(
            success=False,
            error=f"Pipeline error: {str(e)}",
        )


@app.get("/api/suggested-questions")
def suggested_questions():
    """Return suggested starter questions for the UI."""
    return {
        "questions": [
            {
                "text": "Should I take a home loan at 8.5% interest rate?",
                "category": "Loans",
                "icon": "🏠",
            },
            {
                "text": "What is a good CIBIL score and how can I improve mine?",
                "category": "Credit Score",
                "icon": "📊",
            },
            {
                "text": "Compare SIP vs Fixed Deposit for a 5-year investment",
                "category": "Investments",
                "icon": "📈",
            },
            {
                "text": "How much term insurance cover do I need?",
                "category": "Insurance",
                "icon": "🛡️",
            },
            {
                "text": "Best tax saving investments under Section 80C",
                "category": "Tax Planning",
                "icon": "💰",
            },
            {
                "text": "Is it better to prepay my home loan or invest in mutual funds?",
                "category": "Financial Planning",
                "icon": "🤔",
            },
        ]
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
