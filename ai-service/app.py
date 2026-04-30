import time
from collections import deque
from flask import Flask, request, jsonify, g
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from middleware.sanitizer import sanitize_input

# Import Blueprints
from routes.describe import describe_bp
from routes.recommend import recommend_bp
from routes.generate_report import generate_report_bp
from routes.health import health_bp
from services.embeddings_service import embeddings_service

app = Flask(__name__)

# Security Configuration (ZAP fixes)
app.debug = False
app.config['DEBUG'] = False
app.config['START_TIME'] = time.time()
app.config['REQUEST_TIMES'] = deque(maxlen=100)

# Register Blueprints
app.register_blueprint(describe_bp)
app.register_blueprint(recommend_bp)
app.register_blueprint(generate_report_bp)
app.register_blueprint(health_bp)

# Pre-load Model at Startup
with app.app_context():
    embeddings_service.preload()

# Rate Limiter (Day 3)
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["30 per minute"],
    storage_uri="memory://",
)

# Input Sanitization Middleware (Day 3)
@app.before_request
def before_request():
    g.start_time = time.time()
    
    # Sanitization logic
    if request.is_json:
        data = request.get_json()
        if data:
            for key, value in data.items():
                if isinstance(value, str):
                    sanitized_value = sanitize_input(value)
                    if sanitized_value is None:
                        return jsonify({
                            "error": "Security validation failed",
                            "message": "Potential prompt injection detected."
                        }), 400
                    data[key] = sanitized_value

@app.after_request
def after_request(response):
    # Record performance stats for /health endpoint
    if hasattr(g, 'start_time'):
        elapsed = time.time() - g.start_time
        app.config['REQUEST_TIMES'].append(elapsed)
    
    # Security Headers (ZAP fixes)
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Content-Security-Policy'] = "default-src 'self'; script-src 'none'; object-src 'none';"
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains; preload'
    response.headers['Referrer-Policy'] = 'no-referrer'
    response.headers['Permissions-Policy'] = 'geolocation=(), microphone=(), camera=()'
    return response

@app.route('/')
def home():
    return {"message": "Privacy Assessment AI Service Running"}

if __name__ == '__main__':
    app.run(port=5000, debug=False)