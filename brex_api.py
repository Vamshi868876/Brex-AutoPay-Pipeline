import requests
import uuid
import hashlib
from config import BREX_BASE_URL, BREX_USER_TOKEN, TEST_MODE

class BrexAPI:
    def __init__(self):
        self.base_url = BREX_BASE_URL
        self.token = BREX_USER_TOKEN
        
    def get_headers(self):
        return {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
        
    def get_vendor_id_by_name(self, vendor_name):
        url = f"{self.base_url}/v1/vendors"
        cursor = None
        
        # Clean string for fuzzy match
        search_name = vendor_name.lower().replace("inc.", "").replace("inc", "").replace("llc", "").replace(",", "").replace(".", "").strip()
        
        while True:
            params = {"limit": 100}
            if cursor:
                params["cursor"] = cursor
                
            response = requests.get(url, headers=self.get_headers(), params=params)
            if response.status_code != 200:
                print(f"Error fetching vendors: {response.status_code} - {response.text}")
                return None
                
            data = response.json()
            vendors = data.get("items", [])
            
            for v in vendors:
                brex_name = v.get("company_name", "").lower().replace("inc.", "").replace("inc", "").replace("llc", "").replace(",", "").replace(".", "").strip()
                # Use simple inclusion for fuzzy matching
                if brex_name and (search_name in brex_name or brex_name in search_name):
                    payment_accounts = v.get("payment_accounts", [])
                    if payment_accounts:
                        # Extract payment_instrument_id from the details object
                        details = payment_accounts[0].get("details", {})
                        payment_instrument_id = details.get("payment_instrument_id")
                        if payment_instrument_id:
                            return payment_instrument_id
                    
                    print(f"\n[ERROR] Vendor '{v.get('company_name')}' was found in Brex, but they have NO bank details (ACH/Wire) saved! Brex cannot send them money.")
                    return None
                    
            cursor = data.get("next_cursor")
            if not cursor:
                break
                
        return None
        
    def create_vendor_payment(self, payload):
        """
        Creates an approved bill/payment in Brex using the extracted OCR data.
        """
        url = f"{self.base_url}/v1/transfers"
        
        # Ramp-style Duplicate Prevention!
        # Instead of a random UUID, we generate a unique hash based on the Invoice Memo.
        # This guarantees that if the script runs 100 times on the exact same invoice,
        # Brex will instantly block it as a duplicate!
        invoice_string = payload.get("external_memo", "unknown")
        idemp_key = hashlib.md5(invoice_string.encode('utf-8')).hexdigest()
        
        headers = self.get_headers()
        headers["Idempotency-Key"] = idemp_key
        
        if TEST_MODE:
            print(f"==================================================")
            print(f"[TEST MODE ACTIVE] No money will be transferred!")
            print(f"Bot WOULD HAVE successfully paid ${payload.get('amount')} to {payload.get('vendor_name')} for Invoice #{payload.get('invoice_number')}.")
            print(f"==================================================")
            return {"id": "mock_brex_transfer_123", "status": "TEST_MODE_APPROVED"}

        if not self.token or self.token == "your_brex_user_token_here":
            print(f"[ERROR] Invalid Token!")
            return None
            
        # Example endpoint - check developer.brex.com for your specific company's endpoint (transfers vs payments)
        url = f"{self.base_url}/v1/transfers"
        
        try:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            print(f"Brex API Error: {e.response.text}")
            raise e
