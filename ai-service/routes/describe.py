import os
import json
import requests
from datetime import datetime, timezone
from flask import Blueprint, request, jsonify
from dotenv import load_dotenv

load_dotenv()

describe_bp = Blueprint('describe', __name__)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

@describe_bp.route('/describe', methods=['POST'])
def describe():
    """
    Day 3 Task: POST /describe — validate input, load prompt, call Groq, return structured JSON with generated_at
    """
    data = request.get_json()
    
    # 1. Validate Input
    if not data or "input" not in data:
        return jsonify({"error": "Missing 'input' field in JSON request body."}), 400
    
    user_input = data["input"]
    
    # 2. Load Prompt Robustly
    try:
        base_dir = os.path.dirname(os.path.dirname(__file__))
        prompt_path = os.path.join(base_dir, "prompts", "describe_prompt.txt")
        with open(prompt_path, "r") as f:
            prompt_template = f.read()
    except Exception as e:
        return jsonify({"error": f"Failed to load prompt template: {str(e)}"}), 500
        
    prompt = prompt_template.replace("{user_input}", str(user_input))
    
    # 2.5 Check Redis Cache (Day 7 Task)
    try:
        import time
        from services.ai_cache import get_cached_response, set_cached_response, record_response_time
        cached = get_cached_response(prompt)
        if cached:
            print("Cache hit! Returning Redis data.")
            return jsonify(cached), 200
    except Exception:
        pass
    
    # Check for API Key
    if not GROQ_API_KEY:
        return handle_fallback("Missing GROQ_API_KEY environment variable. Cannot contact LLM.")
        
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
    
    # 3. Call Groq
    t0 = time.time()
    try:
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=10
        )
        response.raise_for_status()
        
        # Log response metric
        record_response_time(time.time() - t0)
        
        # 4. Extract and Strip Response
        data_resp = response.json()
        raw_text = data_resp['choices'][0]['message']['content']
        
        # Strip away markdown block
        clean_response = raw_text.strip("` \n")
        if clean_response.lower().startswith("json"):
            clean_response = clean_response[4:].strip()
            
        assessment_data = json.loads(clean_response)
        
        # 5. Return structured JSON with `generated_at`!
        assessment_data["generated_at"] = datetime.now(timezone.utc).isoformat()
        
        # 6. Save back to Redis cache (Day 7)
        try:
            set_cached_response(prompt, assessment_data, 900)
        except Exception:
            pass
        
        return jsonify(assessment_data), 200
        
    except requests.exceptions.RequestException as e:
        return handle_fallback(f"Groq API connection failure: {str(e)}")
    except json.JSONDecodeError as e:
        return handle_fallback(f"AI returned invalid JSON: {str(e)}")
    except Exception as e:
        return handle_fallback(f"Unexpected processing error: {str(e)}")

def handle_fallback(error_message):
    """
    Day 9 Task: Never return HTTP 500 when AI is unavailable.
    Return the fallback template with {is_fallback: true}
    """
    print(f"Fallback triggered due to: {error_message}")
    
    fallback_response = {
        "is_fallback": True,
        "summary": "AI Assessment is temporarily unavailable. Please review this record manually.",
        "data_collected": ["Unknown"],
        "privacy_risks": ["Unable to determine automatic risk. Consult security team."],
        "risk_level": "Medium",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "error_detail": error_message
    }
    
    # We still return HTTP 200 status as requested in the sprint requirements, 
    # to let the frontend render the fallback data smoothly.
    return jsonify(fallback_response), 200
