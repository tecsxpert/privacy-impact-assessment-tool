import os
import requests
from dotenv import load_dotenv

load_dotenv()

def test_groq():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print("Error: GROQ_API_KEY not found in .env")
        return

    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [{"role": "user", "content": "Hello"}],
        "max_tokens": 5
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            print("✅ Groq API call successful!")
        else:
            print(f"❌ API call failed: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    test_groq()
