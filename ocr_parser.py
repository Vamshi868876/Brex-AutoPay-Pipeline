import fitz  # PyMuPDF
from openai import OpenAI
import json
from config import OPENAI_API_KEY

def extract_text_from_pdf(pdf_path):
    """Extracts raw text from a PDF file."""
    try:
        doc = fitz.open(pdf_path)
        text = ""
        for page in doc:
            text += page.get_text()
        return text
    except Exception as e:
        print(f"Error reading PDF {pdf_path}: {e}")
        return ""

def parse_invoice_data(pdf_path):
    """
    Reads the PDF and uses OpenAI to extract structured data.
    Returns a dictionary with vendor_name, invoice_number, and amount.
    """
    if not OPENAI_API_KEY or OPENAI_API_KEY == "your_openai_api_key_here":
        print("Missing OpenAI API Key. Returning mock data for testing.")
        return {
            "vendor_name": "Test Vendor LLC",
            "invoice_number": "TEST-1234",
            "amount": 500.00,
            "issued_at": "2026-07-16"
        }
        
    raw_text = extract_text_from_pdf(pdf_path)
    if not raw_text.strip():
        print(f"Failed to extract text from {pdf_path}")
        return None
        
    client = OpenAI(api_key=OPENAI_API_KEY)
    
    prompt = f"""
    You are an Accounts Payable OCR engine. Extract the following details from this invoice text:
    - Vendor Name
    - Invoice Number
    - Total Amount (as a float, no currency symbols)
    - Invoice Date (YYYY-MM-DD format)
    
    Respond ONLY in valid JSON format like this:
    {{"vendor_name": "Apple Inc", "invoice_number": "INV-100", "amount": 1200.50, "issued_at": "2026-07-16"}}
    
    Invoice Text:
    {raw_text}
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            response_format={ "type": "json_object" }
        )
        
        result_json = response.choices[0].message.content
        return json.loads(result_json)
        
    except Exception as e:
        if "insufficient_quota" in str(e):
            print(f"\n[AI WARNING] Your OpenAI account has $0.00 credits! (Error 429)")
            print(f"Skipping AI and returning MOCK data so you can see the bot finish its job!\n")
            return {
                "vendor_name": "ORPINE INC (Mocked)",
                "invoice_number": "2026-534",
                "amount": 12800.00,
                "issued_at": "2026-06-06"
            }
        print(f"OpenAI API Error: {e}")
        return None
