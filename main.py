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
        
        # 3. Lookup Vendor ID dynamically
        vendor_name = invoice_data.get("vendor_name", "")
        print(f"Looking up Brex Vendor ID for '{vendor_name}'...")
        vendor_id = brex.get_vendor_id_by_name(vendor_name)
        
        if not vendor_id:
            print(f"Vendor '{vendor_name}' not found in Brex. Skipping payment. Please add them to Brex first!")
            continue
            
        print(f"Found Vendor ID: {vendor_id}")
        
        # 4. Push to Brex API (Using the strict v1/transfers schema)
        # Note: Brex requires amounts in cents, and requires specific IDs for vendors and funding accounts.
        amount_in_cents = int(float(invoice_data.get("amount", 0)) * 100)
        
        payload = {
            "amount": {
                "amount": amount_in_cents,
                "currency": "USD"
            },
            "counterparty": {
                "type": "VENDOR",
                "payment_instrument_id": vendor_id # Dynamically fetched!
            },
            "description": f"Invoice {invoice_data.get('invoice_number')}",
            "external_memo": f"Invoice {invoice_data.get('invoice_number')} from {invoice_data.get('vendor_name')}",
            "originating_account": {
                "type": "BREX_CASH",
                "id": "dpacc_cklicxj7n019l01khl9zqxq6x" # Your Primary Checking Account ID
            }
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
