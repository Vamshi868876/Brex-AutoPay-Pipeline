import schedule
import time
import datetime
from email_reader import fetch_unread_invoice_pdfs
from ocr_parser import parse_invoice_data
from brex_api import BrexAPI

brex = BrexAPI()

def run_pipeline():
    print(f"\n[{datetime.datetime.now()}] Checking Gmail for new Brex Invoices...")
    
    # 1. Fetch unread PDFs from Gmail
    pdf_paths = fetch_unread_invoice_pdfs()
    
    if not pdf_paths:
        return
        
    for pdf_path in pdf_paths:
        print(f"Processing {pdf_path}...")
        
        # 2. Extract Data using AI OCR
        invoice_data = parse_invoice_data(pdf_path)
        if not invoice_data:
            print("Failed to extract data. Skipping.")
            continue
            
        print(f"Extracted Data: {invoice_data}")
        
        # 3. Push to Brex API
        payload = {
            "vendor_name": invoice_data.get("vendor_name"),
            "amount": invoice_data.get("amount"),
            "invoice_number": invoice_data.get("invoice_number"),
            "description": f"Invoice {invoice_data.get('invoice_number')}"
        }
        
        print("Pushing to Brex...")
        result = brex.create_vendor_payment(payload)
        if result:
            print(f"SUCCESS! Brex Payment ID: {result.get('id')}")

if __name__ == "__main__":
    print("🚀 Starting Brex Custom AP Automation Pipeline...")
    
    # Run once at startup
    run_pipeline()
    
    # Poll every 5 minutes for new emails
    schedule.every(5).minutes.do(run_pipeline)
    
    while True:
        schedule.run_pending()
        time.sleep(60)
