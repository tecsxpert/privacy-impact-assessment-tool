from flask import Flask, jsonify
from routes.describe import describe_bp
from routes.recommend import recommend_bp
from routes.generate_report import generate_report_bp
from services.ai_cache import CURRENT_MODEL, get_uptime_seconds, get_avg_response_time_ms

app = Flask(__name__)

# Register Blueprints (Day 1)
app.register_blueprint(describe_bp)
app.register_blueprint(recommend_bp)
app.register_blueprint(generate_report_bp)


# Day 7: GET /health — model, avg response time, uptime
@app.route('/health')
def health():
    return jsonify({
        "status": "healthy",
        "model": CURRENT_MODEL,
        "uptime_seconds": round(get_uptime_seconds(), 2),
        "avg_response_time_ms": round(get_avg_response_time_ms(), 2)
    })


# Day 8: Security headers on every response — fixes OWASP ZAP Critical/High findings
@app.after_request
def add_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    response.headers['Content-Security-Policy'] = "default-src 'self'; frame-ancestors 'none'"
    return response


if __name__ == '__main__':
    app.run(port=5000, debug=True)
