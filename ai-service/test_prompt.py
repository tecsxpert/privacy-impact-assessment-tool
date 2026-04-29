import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Read prompt file
try:
    # Use absolute path based on __file__ to ensure robustness
    prompt_path = os.path.join(os.path.dirname(__file__), "prompts", "describe_prompt.txt")
    with open(prompt_path, "r") as file:
        prompt_template = file.read()
except Exception as e:
    print(f"Error loading prompt template: {e}")
    exit(1)

# Create 5 sample test inputs
test_inputs = [
    {
        "recordType": "Employee Data",
        "retentionPeriod": "5 years",
        "riskLevel": "High"
    },
    {
        "recordType": "Financial Records",
        "retentionPeriod": "7 years",
        "riskLevel": "Medium"
    },
    {
        "recordType": "Customer Data",
        "retentionPeriod": "3 years",
        "riskLevel": "High"
    },
    {
        "recordType": "Legal Documents",
        "retentionPeriod": "10 years",
        "riskLevel": "Low"
    },
    {
        "recordType": "Medical Records",
        "retentionPeriod": "8 years",
        "riskLevel": "High"
    }
]

def call_groq(prompt_text):
    if not GROQ_API_KEY:
        return {"error": "Missing GROQ_API_KEY environment variable. Have you created the .env file in ai-service directory and assigned it?"}
        
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # We use llama-3.3-70b-versatile as it maps to the model requested in the Capstone PDF
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "system", "content": "You are a helpful API that returns strictly JSON."},
            {"role": "user", "content": prompt_text}
        ],
        "temperature": 0.3
    }
    
    try:
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=10
        )
        response.raise_for_status()
        data = response.json()
        raw_text = data['choices'][0]['message']['content']
        
        # Strip away markdown json backticks if hallucinated by LLM
        clean_response = raw_text.strip("` \n")
        if clean_response.lower().startswith("json"):
            clean_response = clean_response[4:].strip()
            
        return json.loads(clean_response)
    
    except requests.exceptions.RequestException as e:
        return {"error": f"API Request failed: {e}"}
    except json.JSONDecodeError as e:
        return {"error": f"Failed to parse JSON response: {e}. Raw response was: {raw_text}"}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}

print("Starting to test the primary prompt with 5 inputs...\n" + "="*50)

for i, test in enumerate(test_inputs, 1):
    print(f"\n--- Test Case {i} ---")
    user_input_str = json.dumps(test, indent=2)
    prompt = prompt_template.replace("{user_input}", user_input_str)
    
    print(f"Input configuration:\n{user_input_str}\n")
    
    print("Calling Groq API... ", end="", flush=True)
    result = call_groq(prompt)
    
    if "error" in result:
        print(f"❌ Failed\nDetails: {result['error']}")
    else:
        # Schema Validation
        required_keys = ["summary", "data_collected", "privacy_risks", "risk_level"]
        has_all_keys = all(k in result for k in required_keys)
        
        if has_all_keys:
            print("✅ Success")
            print(f"Parsed JSON keys: {list(result.keys())}")
            print(f"Risk Level Assessed Strategy: {result['risk_level']}")
            print("Summary Snippet: " + str(result['summary'])[:80] + "...")
        else:
            print("❌ Valid JSON generated, but it violated our explicit schema format!")
            missing = [k for k in required_keys if k not in result]
            print(f"Missing keys: {missing}")
            print(f"Actual output keys: {list(result.keys())}")
