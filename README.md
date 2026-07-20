# Brex Custom AP Automation Pipeline

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

An enterprise-grade, fully automated Accounts Payable (AP) pipeline designed specifically for **Brex**. 

Unlike Ramp, Brex's API does not permit developers to access OCR-generated Draft Bills. To bypass this limitation, this architecture implements a **Custom AI Pipeline**. By intercepting vendor invoices via a dedicated Gmail inbox, the Python daemon uses advanced AI (OpenAI GPT-4o / PyMuPDF) to execute its own OCR extraction before pushing a fully approved payment directly to the Brex API.

---

## 🏗️ Architectural Flowchart

```mermaid
graph TD
    %% Styling
    classDef external fill:#f9f9f9,stroke:#333,stroke-width:2px;
    classDef python fill:#4B8BBE,stroke:#306998,stroke-width:2px,color:white;
    classDef openai fill:#10a37f,stroke:#0d8266,stroke-width:2px,color:white;
    classDef brex fill:#F26B43,stroke:#d4512c,stroke-width:2px,color:white;

    %% Nodes
    Vendor([Vendor / Supplier]):::external
    Gmail[📩 Dedicated AP Gmail Inbox]:::external
    Daemon{⚙️ Python Daemon<br/>runs every 5 mins}:::python
    IMAP[📥 email_reader.py<br/>Downloads PDF]:::python
    OCR[🧠 ocr_parser.py<br/>Extracts Text via PyMuPDF]:::python
    GPT[🤖 OpenAI GPT-4o<br/>Structured JSON Extraction]:::openai
    API[💳 brex_api.py<br/>POST /v2/transfers]:::brex
    BrexPlatform[(Brex Dashboard<br/>Payment Sent!)]:::brex

    %% Flow
    Vendor -- "Emails Invoice PDF" --> Gmail
    Gmail -- "IMAP Connection" --> Daemon
    Daemon --> IMAP
    IMAP -- "Passes PDF" --> OCR
    OCR -- "Sends Raw Text" --> GPT
    GPT -- "Returns Amount, Vendor, ID" --> API
    API -- "Executes OAuth Push" --> BrexPlatform
```

---

## 🚀 Features
* **Bypasses Brex Limitations**: Custom OCR engine eliminates the need for Brex's hidden drafts.
* **100% Automated**: Runs as a background daemon polling every 5 minutes.
* **Safe Testing Mode**: Built-in `TEST_MODE` to simulate the pipeline and view AI extraction results without moving real money.
* **Smart Inbox Management**: Only processes the 5 most recent unread emails to prevent memory hangs on large inboxes.

## 🛠️ Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Vamshi868876/brex-payment-automation-.git
   cd brex-payment-automation-
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment:**
   Create a `.env` file in the root directory and populate it with your credentials:
   ```env
   # Brex API Credentials
   BREX_USER_TOKEN=your_brex_user_token_here
   
   # Gmail IMAP Credentials
   EMAIL_ACCOUNT=your_email@gmail.com
   EMAIL_PASSWORD=your_gmail_16_letter_app_password
   
   # OpenAI API Key (For Custom OCR)
   OPENAI_API_KEY=sk-your-openai-key
   ```

4. **Run the Daemon:**
   ```bash
   python main.py
   ```

## 🔒 Security Note (Test Mode)
By default, this repository is configured with `TEST_MODE = True` in `config.py`. This ensures that while you are testing the AI and Email integrations, **no real money will be transferred via Brex**. Once you have verified the AI is extracting vendor names and amounts accurately, switch it to `False` to enable live payments.

## 👨‍💻 Author
Built by **Vamshi Batthula**.
