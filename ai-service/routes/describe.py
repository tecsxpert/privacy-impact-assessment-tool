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
    data = request.get_json()

    # Validate Input
    if not data or "input" not in data:
        return jsonify({"error": "Missing 'input' field in request body."}), 400

    user_input = data["input"]

    # Load Prompt
    try:
        base_dir = os.path.dirname(os.path.dirname(__file__))
        with open(os.path.join(base_dir, "prompts", "describe_prompt.txt"), "r") as f:
            prompt_template = f.read()
    except Exception as e:
        return jsonify({"error": f"Failed to load prompt template: {str(e)}"}), 500

    prompt = prompt_template.replace("{user_input}", str(user_input))

    if not GROQ_API_KEY:
        return handle_fallback("Missing GROQ_API_KEY environment variable.")

    headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
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
            headers=headers, json=payload, timeout=10
        )
        response.raise_for_status()

        raw_text = response.json()['choices'][0]['message']['content']
        clean = raw_text.strip("` \n")
        if clean.lower().startswith("json"):
            clean = clean[4:].strip()

        assessment_data = json.loads(clean)
        assessment_data["generated_at"] = datetime.now(timezone.utc).isoformat()
        return jsonify(assessment_data), 200

    except requests.exceptions.RequestException as e:
        return handle_fallback(f"Groq API connection failure: {str(e)}")
    except json.JSONDecodeError as e:
        return handle_fallback(f"AI returned invalid JSON: {str(e)}")
    except Exception as e:
        return handle_fallback(f"Unexpected error: {str(e)}")


def handle_fallback(error_message):
    print(f"Fallback triggered: {error_message}")
    return jsonify({
        "is_fallback": True,
        "summary": "AI Assessment temporarily unavailable. Please review manually.",
        "data_collected": ["Unknown"],
        "privacy_risks": ["Unable to determine risk automatically."],
        "risk_level": "Medium",
        "generated_at": datetime.now(timezone.utc).isoformat()
    }), 200
