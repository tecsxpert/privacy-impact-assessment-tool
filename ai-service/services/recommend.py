from flask import Blueprint, request, jsonify
from datetime import datetime
import os
import logging
from services.groq_client import groq_client

recommend_bp = Blueprint('recommend', __name__)
logger = logging.getLogger(__name__)

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
        logger.error(f"Prompt file missing: {e}")
        return jsonify({"error": "Prompt file missing"}), 500

    prompt = prompt_template.replace("{user_input}", user_input)

    # ✅ Call Groq AI via shared client
    try:
        recommendations = groq_client.call_ai(prompt, temperature=0.5)
        
        if recommendations is None:
            raise Exception("AI response was empty or failed after retries")

    except Exception as e:
        logger.error(f"AI service failed: {e}")
        return jsonify({
            "error": "AI service failed",
            "details": str(e),
            "is_fallback": True
        }), 500

    # ✅ Return response
    return jsonify({
        "recommendations": recommendations,
        "generated_at": datetime.utcnow().isoformat()
    })