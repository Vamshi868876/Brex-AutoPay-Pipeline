import requests
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
        
    def create_vendor_payment(self, payload):
        """
        Creates an approved bill/payment in Brex using the extracted OCR data.
        """
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
        url = f"{self.base_url}/v2/transfers"
        
        try:
            response = requests.post(url, headers=self.get_headers(), json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            print(f"Brex API Error: {e.response.text}")
            raise e
