import requests
from config import BREX_BASE_URL, BREX_USER_TOKEN

def find_orpine():
    url = f"{BREX_BASE_URL}/v1/vendors"
    headers = {
        "Authorization": f"Bearer {BREX_USER_TOKEN}",
        "Content-Type": "application/json"
    }
    
    print("Searching for Orpine in all pages of vendors...\n")
    cursor = None
    found = False
    
    while True:
        params = {"limit": 100}
        if cursor:
            params["cursor"] = cursor
            
        response = requests.get(url, headers=headers, params=params)
        data = response.json()
        
        vendors = data.get("items", [])
        for v in vendors:
            if "orpine" in v.get("company_name", "").lower():
                print(f"FOUND IT!")
                print(f"Vendor Name: {v.get('company_name')}")
                print(f"Vendor ID: {v.get('id')}")
                payment_accounts = v.get("payment_accounts", [])
                for pa in payment_accounts:
                    print(f"  -> Payment Instrument ID: {pa.get('id')} ({pa.get('type')})")
                print("-" * 40)
                found = True
        
        cursor = data.get("next_cursor")
        if not cursor:
            break
            
    if not found:
        print("Orpine not found in API.")

if __name__ == "__main__":
    find_orpine()
