import requests
from config import BREX_BASE_URL, BREX_USER_TOKEN

def list_cash_accounts():
    url = f"{BREX_BASE_URL}/v2/accounts/cash"
    headers = {
        "Authorization": f"Bearer {BREX_USER_TOKEN}",
        "Content-Type": "application/json"
    }
    
    print("Fetching Cash Accounts from Brex...\n")
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        accounts = response.json().get("items", [])
        if not accounts:
            print("No cash accounts found.")
            return
            
        for acc in accounts:
            print(f"Account Name: {acc.get('name', 'Brex Cash')}")
            print(f"Account ID: {acc.get('id')}")
            print(f"Status: {acc.get('status')}")
            print("-" * 40)
    else:
        print(f"Error: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    list_cash_accounts()
