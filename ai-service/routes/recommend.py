import os
import json
import requests
from flask import Blueprint, request, jsonify
from dotenv import load_dotenv

load_dotenv()

recommend_bp = Blueprint('recommend', __name__)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

@recommend_bp.route('/recommend', methods=['POST'])
def recommend():
    """
    Day 4 Task: Build POST /recommend — 3 recommendations as JSON array
    Day 9 Task: Safe fallback without returning 500 error.
    """
    data = request.get_json()
    
    # Validation
    if not data or "input" not in data:
        return jsonify({"error": "Missing 'input' field in request body."}), 400
        
    user_input = data["input"]
    
    # Robust Path Loading
    try:
        base_dir = os.path.dirname(os.path.dirname(__file__))
        prompt_path = os.path.join(base_dir, "prompts", "recommend_prompt.txt")
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
            {"role": "system", "content": "You are a helpful API that returns strictly valid JSON arrays."},
            {"role": "user", "content": prompt}
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
        
        data_resp = response.json()
        raw_text = data_resp['choices'][0]['message']['content']
        
        clean_response = raw_text.strip("` \n")
        if clean_response.lower().startswith("json"):
            clean_response = clean_response[4:].strip()
            
        recommendations = json.loads(clean_response)
        
        return jsonify(recommendations), 200

    except requests.exceptions.RequestException as e:
        return handle_fallback(f"Groq API connection failure: {str(e)}")
    except json.JSONDecodeError as e:
        return handle_fallback(f"AI returned invalid JSON array: {str(e)}")
    except Exception as e:
        return handle_fallback(f"Unexpected processing error: {str(e)}")

def handle_fallback(error_message):
    print(f"Fallback triggered due to: {error_message}")
    fallback_recommendations = [
        {
            "action_type": "Manual Review Required",
            "description": "AI recommendation engine is temporarily offline. Please assess manually.",
            "priority": "High",
            "is_fallback": True
        }
    ]
    return jsonify(fallback_recommendations), 200
