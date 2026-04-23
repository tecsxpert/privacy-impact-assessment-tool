from flask import Blueprint, request, jsonify
from datetime import datetime
import os
import requests
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

describe_bp = Blueprint('describe', __name__)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

@describe_bp.route('/describe', methods=['POST'])
def describe():

    # ✅ Input validation
    data = request.get_json()
    if not data or "input" not in data:
        return jsonify({"error": "Missing input"}), 400

    user_input = data["input"]

    # ✅ Load prompt
    try:
        with open("prompts/describe_prompt.txt", "r") as f:
            prompt_template = f.read()
    except Exception as e:
        return jsonify({
            "error": "Prompt file missing",
            "details": str(e)
        }), 500

    prompt = prompt_template.replace("{user_input}", user_input)

    # ✅ Check API key
    if not GROQ_API_KEY:
        return jsonify({
            "error": "GROQ_API_KEY not found in .env"
        }), 500

    # ✅ Call Groq API safely
    try:
        url = "https://api.groq.com/openai/v1/chat/completions"

        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "llama-3.3-70b-versatile",
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.3
        }

        response = requests.post(
            url,
            headers=headers,
            json=payload,
            timeout=30
        )

        # 🔍 Debug logs (remove later if needed)
        print("STATUS:", response.status_code)
        print("RESPONSE:", response.text)

        result = response.json()

        # ❌ Handle Groq error response
        if "choices" not in result:
            return jsonify({
                "error": "Groq API error",
                "details": result,
                "is_fallback": True
            }), 500

        # ✅ Extract AI response
        raw_output = result["choices"][0]["message"]["content"]

        # ✅ Convert string JSON → actual JSON
        try:
            ai_output = json.loads(raw_output)
        except:
            ai_output = {
                "raw": raw_output,
                "note": "AI returned non-JSON format"
            }

    except Exception as e:
        return jsonify({
            "error": "AI service failed",
            "details": str(e),
            "is_fallback": True
        }), 500

    # ✅ Final response
    return jsonify({
        "result": ai_output,
        "generated_at": datetime.utcnow().isoformat()
    })