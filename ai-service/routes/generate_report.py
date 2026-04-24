import os
import json
import requests
from flask import Blueprint, request, jsonify
from dotenv import load_dotenv

load_dotenv()

generate_report_bp = Blueprint('generate_report', __name__)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

@generate_report_bp.route('/generate-report', methods=['POST'])
def generate_report():
    """
    Day 6 Task: Build POST /generate-report — structured JSON
    Day 9 Task: Safe fallback handling.
    """
    data = request.get_json()
    
    if not data or "input" not in data:
        return jsonify({"error": "Missing 'input' field in request body."}), 400
        
    user_input = data["input"]
    
    try:
        base_dir = os.path.dirname(os.path.dirname(__file__))
        prompt_path = os.path.join(base_dir, "prompts", "generate_report_prompt.txt")
        with open(prompt_path, "r") as f:
            prompt_template = f.read()
    except Exception as e:
        return jsonify({"error": f"Failed to load prompt template: {str(e)}"}), 500
        
    prompt = prompt_template.replace("{user_input}", str(user_input))
    
    if not GROQ_API_KEY:
        return handle_fallback("Missing GROQ_API_KEY environment variable.")

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "system", "content": "You are a helpful API that returns strictly valid JSON."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.3
    }

    try:
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=15 # slightly longer timeout for a full report
        )
        response.raise_for_status()
        
        data_resp = response.json()
        raw_text = data_resp['choices'][0]['message']['content']
        
        clean_response = raw_text.strip("` \n")
        if clean_response.lower().startswith("json"):
            clean_response = clean_response[4:].strip()
            
        report = json.loads(clean_response)
        
        return jsonify(report), 200

    except requests.exceptions.RequestException as e:
        return handle_fallback(f"Groq API connection failure: {str(e)}")
    except json.JSONDecodeError as e:
        return handle_fallback(f"AI returned invalid JSON array: {str(e)}")
    except Exception as e:
        return handle_fallback(f"Unexpected processing error: {str(e)}")

def handle_fallback(error_message):
    print(f"Fallback triggered due to: {error_message}")
    fallback_report = {
        "title": "Privacy Impact Assessment Report (Fallback)",
        "summary": "AI generation is currently offline. Manual review required.",
        "overview": "The system was unable to contact the Groq API to automatically generate this report.",
        "key_items": ["API Connectivity Error", "Service Disruption"],
        "recommendations": ["Review the record manually", "Check AI service health logs"],
        "is_fallback": True
    }
    return jsonify(fallback_report), 200
