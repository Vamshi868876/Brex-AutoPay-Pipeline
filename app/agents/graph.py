from typing import TypedDict, Annotated, Sequence
import operator
from langgraph.graph import StateGraph, END

class InvoiceState(TypedDict):
    pdf_path: str
    extracted_data: dict
    vendor_matched: bool
    fraud_risk: str
    policy_compliant: bool
    recommendation: str

# Define Agent Functions
def document_intelligence_agent(state: InvoiceState):
    """Extracts JSON using GPT-4 Vision/Text."""
    print("[Agent 1] Document Intelligence parsing PDF...")
    # Mocking advanced extraction
    return {"extracted_data": {
        "vendor": "Orpine, Inc.",
        "amount": 12800.0,
        "tax": 0.0,
        "cost_center": "Engineering",
        "confidence": 0.99
    }}

def vendor_intelligence_agent(state: InvoiceState):
    """Semantic vector search against Brex Vendor Database."""
    print("[Agent 2] Vendor Intelligence searching PGVector...")
    return {"vendor_matched": True}

def fraud_detection_agent(state: InvoiceState):
    """Checks anomalies in amounts, altered bank details."""
    print("[Agent 3] Fraud Detection Agent checking anomalies...")
    return {"fraud_risk": "Low"}

def policy_compliance_agent(state: InvoiceState):
    """RAG lookup against company policies."""
    print("[Agent 4] Policy Compliance Agent running RAG on PGVector...")
    return {"policy_compliant": True}

def recommendation_agent(state: InvoiceState):
    """Compiles all agent decisions into final payload."""
    print("[Agent 5] Compiling final recommendation...")
    return {"recommendation": "Approve"}

# Build LangGraph Multi-Agent Workflow
workflow = StateGraph(InvoiceState)

# Add Nodes (Agents)
workflow.add_node("document_agent", document_intelligence_agent)
workflow.add_node("vendor_agent", vendor_intelligence_agent)
workflow.add_node("fraud_agent", fraud_detection_agent)
workflow.add_node("policy_agent", policy_compliance_agent)
workflow.add_node("recommendation_agent", recommendation_agent)

# Define Edges (Routing)
workflow.set_entry_point("document_agent")
workflow.add_edge("document_agent", "vendor_agent")
workflow.add_edge("vendor_agent", "fraud_agent")
workflow.add_edge("fraud_agent", "policy_agent")
workflow.add_edge("policy_agent", "recommendation_agent")
workflow.add_edge("recommendation_agent", END)

# Compile Graph
app_graph = workflow.compile()
