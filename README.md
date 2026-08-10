<div align="center">
  <img src="https://img.shields.io/badge/Brex-000000?style=for-the-badge&logo=brex&logoColor=white" alt="Brex">
  <img src="https://img.shields.io/badge/OpenAI-412991?style=for-the-badge&logo=openai&logoColor=white" alt="OpenAI">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI">
  <img src="https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white" alt="PostgreSQL">
  <br>
  <h1>🚀 Brex AutoPay Pipeline (Enterprise Multi-Agent AI Engine)</h1>
  <p><b>An Autonomous, LangGraph-Driven Financial Pipeline for Zero-Touch Invoice Processing</b></p>
  <p><i>Developed by <b>Vamshi Batthula</b> (<a href="mailto:batthulavamshi740@gmail.com">batthulavamshi740@gmail.com</a>)</i></p>
</div>

---

## 📖 About The Project
The **Brex AutoPay Pipeline** is an elite, fully autonomous Accounts Payable (AP) engine engineered to eradicate manual data entry and enforce zero-defect financial workflows. Designed with the architectural rigor of top-tier FAANG and fintech platforms, this pipeline transforms raw, unstructured invoice data into secure, ledger-ready draft payments with zero human intervention.

Moving beyond simple OCR scripts, this architecture utilizes a **Multi-Agent RAG Ecosystem** powered by LangGraph, PGVector, and FastAPI. It harmonizes advanced AI for data extraction, semantic duplicate prevention, real-time fraud detection, and policy compliance, showcasing a production-ready, highly secure bridge between standard email protocols and modern corporate banking APIs.

### 🌟 Key Technologies & Topics
`Python` `FastAPI` `LLMs` `GPT-4` `Generative AI` `RAG` `LangChain` `LangGraph` `Multi-Agent AI` `PGVector` `PostgreSQL` `Vector Search` `OCR` `Prompt Engineering` `Document AI` `Intelligent Document Processing (IDP)` `Brex API` `REST APIs` `Redis` `Docker`

---

## 🧠 System Architecture & Multi-Agent Workflow

The architecture operates using an orchestration of specialized AI Agents. Each agent is responsible for a strict validation boundary, ensuring funds never leave the account without passing rigorous, AI-driven compliance checks.

```mermaid
%%{init: {'theme': 'base', 'themeVariables': { 'primaryColor': '#ffffff', 'primaryBorderColor': '#333333', 'lineColor': '#F2613F', 'fontFamily': 'Inter, sans-serif'}}}%%
flowchart TD
    %% Define Node Styles
    classDef ingestion fill:#E8EAF6,stroke:#3F51B5,stroke-width:2px,color:#1A237E
    classDef agent fill:#E0F7FA,stroke:#00BCD4,stroke-width:2px,color:#006064
    classDef rag fill:#FFF3E0,stroke:#FF9800,stroke-width:2px,color:#E65100
    classDef brex fill:#FBE9E7,stroke:#FF5722,stroke-width:2px,color:#BF360C
    
    subgraph Phase_1 [Phase 1: Ingestion]
        A([📧 Vendors Email Invoice]):::ingestion --> B{IMAP Listener}:::ingestion
        B --> C[(Raw PDFs)]:::ingestion
    end

    subgraph Phase_2 [Phase 2: Multi-Agent AI (LangGraph)]
        D[📄 Document Intelligence Agent]:::agent
        E[🏢 Vendor Intelligence Agent]:::agent
        F[🚨 Fraud Detection Agent]:::agent
        G[📜 Policy Compliance Agent]:::agent
        H[📊 Approval Recommendation Agent]:::agent
        
        C --> D
        D -->|JSON Extraction| E
        E -->|Semantic Match| F
        F -->|Anomaly Check| G
        G <-->|RAG Query| I[(PGVector Policies & Contracts)]:::rag
        G --> H
    end

    subgraph Phase_3 [Phase 3: Secure Execution]
        J{Semantic Duplicate Detection}:::rag
        K((Brex /v1/transfers)):::brex
        L[Brex Pending Approval Queue]:::brex
        M((Human Approval)):::brex
        
        H -->|Decision Summary| J
        J <-->|Vector Search| N[(PGVector Ledger)]:::rag
        J -->|Hash & Semantic Match| K
        K --> L
        L -.-> M
    end
```

---

## 🔥 Advanced Enterprise AI Features

### 1. Multi-Agent Orchestration (LangGraph)
Instead of a single LLM prompt, the system utilizes specialized agents passing context:
- **Document Agent:** Extracts high-fidelity JSON (Vendor, Tax, Category, Cost Center, Risk Confidence, Missing Fields).
- **Vendor Agent:** Validates vendor legitimacy against internal CRM databases.
- **Fraud Agent:** Detects forged invoices, suspicious amounts, or altered ACH details.
- **Policy Agent (RAG):** Queries company expense policies to ensure the purchase is authorized.
- **Recommendation Agent:** Compiles findings into a comprehensive decision payload.

### 2. Semantic Duplicate Detection (PGVector)
Standard MD5 hashing fails if an invoice number changes by a single character. This system embeds the semantic meaning of the invoice using Vector Embeddings. Even if a vendor submits an altered PDF, the **Vector Search** will flag it as a duplicate based on meaning, completely neutralizing duplicate fraud.

### 3. AI Approval Summaries
Instead of a simple "Drafted" state, the pipeline injects a rich AI summary directly into the Brex dashboard memo:
* **Policy:** Compliant
* **Fraud Risk:** Low
* **Duplicate Risk:** None
* **Recommendation:** Approve (Confidence: 98%)

### 4. Enterprise Data Chat (RAG)
Features a built-in `/chat` API endpoint allowing executives to converse with their financial data:
> *"Why wasn't invoice 423 approved?"*
> *"Find all Adobe invoices above ₹50,000 from Q3."*

### 5. Classical ML Integration
Harmonizes Generative AI with Classical Machine Learning to predict:
- Late Payment Probabilities
- Vendor Risk Scores
- Cash Flow Optimization

---

## ⚡ Quick Start Guide

### 1. Requirements
- Python 3.12+
- Docker (For PostgreSQL & PGVector)
- A Brex Account (with `Account Admin` privileges)
- OpenAI API Key

### 2. Secure Configuration
Clone the repository and create a `.env` file at the root. **This file is automatically protected by `.gitignore`**.

```env
BREX_USER_TOKEN=your_brex_token
EMAIL_ACCOUNT=ap@yourcompany.com
EMAIL_PASSWORD=your_gmail_app_password
OPENAI_API_KEY=sk-your-openai-key
DATABASE_URL=postgresql://user:pass@localhost:5432/brex_autopay
```

### 3. Execution
```bash
pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```
---
<div align="center">
  <i>Engineered for precision. Built for scale.</i>
</div>
