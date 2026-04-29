import os
import sys
import json

# Add the parent directory to the path so we can import services and prompts
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.groq_client import groq_client
from prompts import get_pia_system_prompt

INPUTS = [
    "We are building a mobile application that uses GPS to track user location continuously and shares it with third-party advertisers.",
    "Our new HR system will store employee social security numbers, bank details, and health records in a centralized cloud database.",
    "A fitness tracker that monitors heart rate and sleep patterns. Data is synced to our servers and used to recommend workout plans.",
    "An e-commerce website that collects customer names, addresses, and credit card info for order processing, using Stripe for payments.",
    "A smart home device with a microphone that records audio constantly to detect wake words and sends snippets to the cloud for processing.",
    "A public forum where users can post anonymously, but we log IP addresses and browser fingerprints for anti-spam purposes.",
    "A marketing campaign that scrapes public social media profiles to build a database of potential leads including email and phone numbers.",
    "A children's educational game that asks for the child's age, name, and school, and displays leaderboards publicly.",
    "A facial recognition system used at office entrances to replace ID badges, storing biometric templates locally on the device.",
    "A web analytics tool that uses first-party cookies to track user journey across our site, without collecting PII."
]

def evaluate_response(response, original_input):
    """
    Evaluates the AI's response heuristically.
    Returns a score out of 10.
    """
    score = 10
    reasons = []

    if not response or "choices" not in response:
        return 0, ["Invalid or empty response"]

    content = response["choices"][0]["message"]["content"]
    
    try:
        data = json.loads(content)
        
        # Check required fields
        required_fields = ["project_summary", "data_collected", "privacy_risks", "overall_risk_level", "recommendations"]
        for field in required_fields:
            if field not in data:
                score -= 2
                reasons.append(f"Missing required field: {field}")
        
        if "privacy_risks" in data and isinstance(data["privacy_risks"], list):
            if len(data["privacy_risks"]) == 0:
                score -= 1
                reasons.append("No privacy risks identified")
        else:
            score -= 2
            reasons.append("privacy_risks is not a list")
            
        if data.get("overall_risk_level") not in ["High", "Medium", "Low"]:
            score -= 1
            reasons.append("Invalid overall_risk_level value")
            
    except json.JSONDecodeError:
        score -= 5
        reasons.append("Response is not valid JSON")

    return max(0, score), reasons

def run_tuning():
    print("Starting Prompt Tuning...")
    total_score = 0
    
    for i, user_input in enumerate(INPUTS):
        print(f"\n--- Input {i+1} ---")
        print(f"Text: {user_input}")
        
        prompt = get_pia_system_prompt(user_input)
        response = groq_client.call_ai(prompt)
        
        score, reasons = evaluate_response(response, user_input)
        print(f"Score: {score}/10")
        if reasons:
            print(f"Deductions: {reasons}")
            
        total_score += score
        
    avg_score = total_score / len(INPUTS)
    print(f"\nAverage Score: {avg_score}/10")
    
    if avg_score < 7:
        print("FAIL: Prompt needs tuning (Score < 7)")
        sys.exit(1)
    else:
        print("SUCCESS: Prompt is effective (Score >= 7)")
        sys.exit(0)

if __name__ == "__main__":
    run_tuning()
