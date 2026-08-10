from fastapi import FastAPI, BackgroundTasks, Depends
from pydantic import BaseModel
from typing import List, Optional
from app.core.config import settings

app = FastAPI(
    title="Brex AutoPay Pipeline API",
    description="Multi-Agent FAANG AP Engine powered by LangGraph & PGVector",
    version="2.0.0"
)

class InvoiceProcessRequest(BaseModel):
    pdf_path: str
    
class ChatRequest(BaseModel):
    query: str

class ChatResponse(BaseModel):
    response: str
    confidence: float
    sources: List[str]

@app.get("/")
def health_check():
    return {"status": "healthy", "mode": "FAANG-Enterprise"}

from app.agents.graph import app_graph

@app.post("/api/v1/process-invoice")
def process_invoice(request: InvoiceProcessRequest, background_tasks: BackgroundTasks):
    """
    Kicks off the LangGraph Multi-Agent pipeline to process a raw invoice PDF.
    This triggers the Document, Vendor, Fraud, Policy, and Recommendation Agents.
    """
    # Trigger the multi-agent graph with the initial state
    initial_state = {"pdf_path": request.pdf_path}
    background_tasks.add_task(app_graph.invoke, initial_state)
    
    return {
        "status": "processing", 
        "message": f"Invoice {request.pdf_path} submitted to Multi-Agent pipeline for processing.",
        "job_id": "job_12345"
    }

@app.post("/api/v1/chat", response_model=ChatResponse)
def invoice_chat(request: ChatRequest):
    """
    RAG-powered chat endpoint to query historical invoices, contracts, and policies.
    Example: 'Why wasn't invoice 423 approved?'
    """
    # mock response for now until Phase 5 is fully implemented
    return ChatResponse(
        response=f"Based on internal Policy Doc v2, invoice 423 was blocked by the Fraud Agent due to a mismatched ACH routing number for Orpine, Inc.",
        confidence=0.98,
        sources=["PGVector:policy_v2", "PGVector:historical_invoices"]
    )
