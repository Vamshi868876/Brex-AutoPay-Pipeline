<div align="center">
  <img src="https://img.shields.io/badge/Brex-000000?style=for-the-badge&logo=brex&logoColor=white" alt="Brex">
  <img src="https://img.shields.io/badge/OpenAI-412991?style=for-the-badge&logo=openai&logoColor=white" alt="OpenAI">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <br>
  <h1>🚀 Next-Gen Accounts Payable Engine</h1>
  <p><b>An Autonomous, AI-Driven Financial Pipeline for Zero-Touch Invoice Processing</b></p>
</div>

---

## 📖 The Vision
Processing invoices manually is a relic of the past. The **Brex AutoPay Pipeline** is an enterprise-grade automation architecture designed to eliminate data entry, prevent financial leaks, and integrate seamlessly with modern corporate banking platforms. 

Built to rival the proprietary automation of platforms like **Ramp** and **Bill.com**, this engine monitors AP inboxes, uses AI (GPT-4) to extract unstructured PDF data, performs fuzzy-matching against internal Vendor Directories, and stages secure, idempotent draft payments directly in the Brex banking dashboard.

---

## 🧠 System Architecture & Workflow

The architecture is designed with strict boundaries between data extraction and financial disbursement. The system acts strictly as an intelligent "drafter", ensuring funds never leave the account without final human authorization.

```mermaid
%%{init: {'theme': 'base', 'themeVariables': { 'primaryColor': '#ffffff', 'primaryBorderColor': '#333333', 'lineColor': '#F2613F', 'fontFamily': 'Inter, sans-serif'}}}%%
flowchart TD
    %% Define Node Styles
    classDef email fill:#E8EAF6,stroke:#3F51B5,stroke-width:2px,color:#1A237E
    classDef ai fill:#E0F7FA,stroke:#00BCD4,stroke-width:2px,color:#006064
    classDef brex fill:#FBE9E7,stroke:#FF5722,stroke-width:2px,color:#BF360C
    classDef secure fill:#E8F5E9,stroke:#4CAF50,stroke-width:2px,color:#1B5E20
    
    subgraph Phase 1: Ingestion
        A([📧 Vendors Email Invoice]):::email --> B{IMAP Listener}:::email
        B -->|Downloads| C[(Raw PDFs)]:::email
    end

    subgraph Phase 2: AI Extraction
        C --> D[PyMuPDF Text Extractor]:::ai
        D -->|Raw String| E{OpenAI GPT-4}:::ai
        E -->|JSON Object| F[Data: Vendor, Amount, Date]:::ai
    end

    subgraph Phase 3: Brex Integration
        F --> G[Fuzzy Matching Algorithm]:::brex
        G <-->|Query| H[(Brex Vendor Directory)]:::brex
        G -->|Match Found| I[Extract Hidden ACH Details]:::brex
    end

    subgraph Phase 4: Secure Execution
        I --> J{Idempotency Hash Generator}:::secure
        J -->|Hash: Invoice + Vendor| K((POST /v1/transfers)):::secure
        K --> L[Brex Pending Approval Queue]:::brex
        L -.-> M((Human Approval)):::secure
    end

    Phase 1 --> Phase 2
    Phase 2 --> Phase 3
    Phase 3 --> Phase 4
```

---

## 🛡️ Enterprise Security: Idempotency & Duplicate Prevention

One of the most dangerous risks in AP automation is paying the same invoice twice. This engine solves this completely using **Cryptographic Idempotency**.

Instead of sending generic requests, the pipeline generates a unique MD5 Hash signature for every single invoice based on its Invoice Number and Vendor Name. 

```python
invoice_string = f"Invoice {invoice_number} from {vendor_name}"
idemp_key = hashlib.md5(invoice_string.encode('utf-8')).hexdigest()
```

If the script runs twice on the same email, or if a vendor sends a duplicate PDF, the mathematical hash remains identical. Brex's API instantly recognizes the duplicate Hash and **blocks the second payment from ever being created.** 

---

## ⚡ Quick Start Guide

### 1. Requirements
- Python 3.10+
- A Brex Account (with `Account Admin` privileges for the API Token)
- An AP Gmail Account (with an App Password)
- OpenAI API Key

### 2. Secure Configuration
Clone the repository and create a `.env` file at the root. **This file is automatically protected by `.gitignore`**.

```env
BREX_USER_TOKEN=your_brex_token (Requires full Read/Write for Vendors & Transfers)
EMAIL_ACCOUNT=ap@yourcompany.com
EMAIL_PASSWORD=your_gmail_app_password
OPENAI_API_KEY=sk-your-openai-key
```

### 3. Execution
```bash
pip install -r requirements.txt
python main.py
```

### 4. Observe the Magic
The terminal will output the live extraction and matching process, ending with a success payload. Log into your Brex Dashboard and check the **Tasks / Approvals** tab to view your perfectly drafted, ready-to-approve payments!

---
<div align="center">
  <i>Engineered for precision. Built for scale.</i>
</div>
