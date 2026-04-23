from flask import Blueprint, request, jsonify
from datetime import datetime
import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

recommend_bp = Blueprint('recommend', __name__)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

@recommend_bp.route('/recommend', methods=['POST'])
def recommend():
    data = request.get_json()

    # ✅ Validation
    if not data or "input" not in data:
        return jsonify({"error": "Missing input"}), 400

    user_input = data["input"]

    # ✅ Load prompt
    try:
        with open("prompts/recommend_prompt.txt", "r") as f:
            prompt_template = f.read()
    except Exception as e:
        return jsonify({"error": "Prompt file missing"}), 500

    prompt = prompt_template.replace("{user_input}", user_input)

    # ✅ Direct Call to Groq (AI 1 Task)
    try:
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "llama-3.3-70b-versatile",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.5
        }

        response = requests.post(url, headers=headers, json=payload, timeout=30)
        result = response.json()
        raw_output = result["choices"][0]["message"]["content"]
        
        try:
            recommendations = json.loads(raw_output)
        except:
            recommendations = {"raw": raw_output}

    except Exception as e:
        return jsonify({
            "error": "AI service failed",
            "details": str(e)
        }), 500

    # ✅ Return response
    return jsonify({
        "recommendations": recommendations,
        "generated_at": datetime.utcnow().isoformat()
    })
