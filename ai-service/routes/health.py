import time
import os
import redis
from flask import Blueprint, jsonify, current_app

health_bp = Blueprint('health', __name__)

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
redis_client = redis.from_url(REDIS_URL, decode_responses=True)

@health_bp.route('/health', methods=['GET'])
def health():
    # Calculate Uptime
    start_time = current_app.config.get('START_TIME', time.time())
    uptime_seconds = time.time() - start_time
    
    # Calculate Avg Response Time
    request_times = current_app.config.get('REQUEST_TIMES', [])
    avg_response_time = sum(request_times) / len(request_times) if request_times else 0.0

    # Check Redis
    redis_status = "offline"
    try:
        if redis_client.ping():
            redis_status = "online"
    except Exception:
        pass

    return jsonify({
        "status": "healthy",
        "model": "llama-3.1-8b-instant",
        "uptime_seconds": round(uptime_seconds, 2),
        "avg_response_time_ms": round(avg_response_time * 1000, 2),
        "redis_status": redis_status
    }), 200
