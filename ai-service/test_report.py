import requests
import json

def test_generate_report():
    url = "http://localhost:5000/generate-report"
    payload = {
        "input": {
            "recordType": "Customer Transactions",
            "retentionPeriod": "10 years",
            "riskLevel": "High",
            "summary": "Large scale collection of financial data including credit card numbers and purchase history.",
            "data_collected": ["Credit Card Numbers", "Full Name", "Billing Address", "Purchase Amount"],
            "privacy_risks": ["Potential for financial fraud if data leaked", "Unauthorized access to transaction history"]
        }
    }
    
    print(f"Testing {url} with input data...")
    try:
        response = requests.post(url, json=payload, timeout=20)
        response.raise_for_status()
        print("Success! Response:")
        print(json.dumps(response.json(), indent=4))
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the AI service. Is it running?")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_generate_report()
