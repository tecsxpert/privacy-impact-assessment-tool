from flask import Flask, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from middleware.sanitizer import sanitize_input
from services.groq_client import groq_client
from prompts import get_pia_system_prompt

app = Flask(__name__)

# Rate Limiter (Day 3)
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["30 per minute"],
    storage_uri="memory://",
)

# Input Sanitization Middleware (Day 3)
@app.before_request
def sanitize_middleware():
    if request.is_json:
        data = request.get_json()
        if data:
            # We iterate through all string values in the JSON body
            for key, value in data.items():
                if isinstance(value, str):
                    sanitized_value = sanitize_input(value)
                    
                    if sanitized_value is None:
                        return jsonify({
                            "error": "Security validation failed",
                            "message": "Potential prompt injection detected."
                        }), 400
                    
                    # Update the data with sanitized text
                    data[key] = sanitized_value

@app.route('/')
def home():
    return {"message": "AI Service Running"}

@app.route('/health')
def health():
    return {"status": "healthy"}

@app.route('/analyze', methods=['POST'])
@limiter.limit("30 per minute")
def analyze():
    data = request.get_json()
    if not data or 'input' not in data:
        return jsonify({"error": "Missing 'input' field"}), 400
        
    user_input = data.get("input", "")
    if not user_input.strip():
        return jsonify({"error": "Input cannot be empty"}), 400

    prompt = get_pia_system_prompt(user_input)
    response = groq_client.call_ai(prompt)

    if response:
        return jsonify({
            "status": "processed",
            "received_input": user_input,
            "analysis": response
        })
    else:
        return jsonify({"error": "Failed to get response from AI service"}), 500

if __name__ == '__main__':
    app.run(port=5000, debug=False)