import os
import json
import requests
import hashlib
import redis
from datetime import datetime, timezone
from flask import Blueprint, request, jsonify
from services.vector_store import vector_store
from dotenv import load_dotenv

load_dotenv()

generate_report_bp = Blueprint('generate_report', __name__)
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

redis_client = redis.from_url(REDIS_URL, decode_responses=True, socket_timeout=0.1, socket_connect_timeout=0.1)


@generate_report_bp.route('/generate-report', methods=['POST'])
def generate_report():
    data = request.get_json()

    # Validate Input
    if not data or "input" not in data:
        return jsonify({"error": "Missing 'input' field in request body."}), 400

    user_input = data["input"]
    input_str = json.dumps(user_input) if isinstance(user_input, dict) else str(user_input)

    cache_key = f"ai_cache:generate_report:{hashlib.sha256(input_str.encode('utf-8')).hexdigest()}"
    try:
        cached_resp = redis_client.get(cache_key)
        if cached_resp:
            print("Serving generate-report from cache")
            return jsonify(json.loads(cached_resp)), 200
    except redis.RedisError as e:
        print(f"Redis cache error: {e}")

    # Load Prompt
    try:
        base_dir = os.path.dirname(os.path.dirname(__file__))
        with open(os.path.join(base_dir, "prompts", "generate_report_prompt.txt"), "r") as f:
            prompt_template = f.read()
    except Exception as e:
        return jsonify({"error": f"Failed to load prompt template: {str(e)}"}), 500

    # Handle string or dict input gracefully
    input_str = json.dumps(user_input) if isinstance(user_input, dict) else str(user_input)
    # RAG: Fetch relevant domain knowledge
    try:
        results = vector_store.query(input_str, n_results=3)
        context = "\n".join(results['documents'][0]) if results['documents'] else ""
    except Exception as e:
        print(f"Vector store query failed: {e}")
        context = ""

    prompt = prompt_template.replace("{user_input}", input_str)
    if context:
        prompt = f"Context from privacy regulations:\n{context}\n\nTask: {prompt}"

    if not GROQ_API_KEY:
        return handle_fallback("Missing GROQ_API_KEY environment variable.")

    headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
    payload = {
        "model": "llama-3.1-8b-instant",
        "messages": [
            {"role": "system", "content": "You are a helpful API that returns strictly valid JSON."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.3
    }

    try:
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers, json=payload, timeout=15
        )
        response.raise_for_status()

        raw_text = response.json()['choices'][0]['message']['content']
        clean = raw_text.strip("` \n")
        if clean.lower().startswith("json"):
            clean = clean[4:].strip()

        report_data = json.loads(clean)
        
        # Add metadata
        report_data["generated_at"] = datetime.now(timezone.utc).isoformat()
        report_data["status"] = "success"
        
        try:
            redis_client.setex(cache_key, 900, json.dumps(report_data))
        except redis.RedisError as e:
            print(f"Redis cache set error: {e}")
        
        return jsonify(report_data), 200

    except requests.exceptions.RequestException as e:
        return handle_fallback(f"Groq API connection failure: {str(e)}")
    except json.JSONDecodeError as e:
        return handle_fallback(f"AI returned invalid JSON: {str(e)}")
    except Exception as e:
        return handle_fallback(f"Unexpected error: {str(e)}")


def handle_fallback(error_message):
    print(f"Fallback triggered for report generation: {error_message}")
    return jsonify({
        "is_fallback": True,
        "title": "Privacy Impact Assessment Report (Fallback)",
        "summary": "The AI service is currently unavailable. Please review the assessment data manually.",
        "overview": "Fallback report generated due to service interruption. AI optimization fallback active.",
        "key_items": ["Review data types manually", "Verify retention policies", "Check encryption status"],
        "recommendations": ["Ensure compliance with local privacy laws", "Conduct manual risk assessment", "Verify data residency"],
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "status": "fallback"
    }), 200
