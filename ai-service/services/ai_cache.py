import redis
import hashlib
import json
import time

# Metrics Globals
start_time = time.time()
total_response_time = 0.0
total_requests = 0
CURRENT_MODEL = "llama-3.3-70b-versatile"

# Initialize Redis gracefully
try:
    redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
    redis_client.ping() # test connection
except Exception as e:
    print(f"Warning: Redis not reachable. Running without cache. ({e})")
    redis_client = None

def get_uptime_seconds():
    return time.time() - start_time

def record_response_time(duration_sec):
    global total_response_time, total_requests
    total_response_time += duration_sec
    total_requests += 1

def get_avg_response_time_ms():
    if total_requests == 0:
        return 0.0
    return (total_response_time / total_requests) * 1000.0

def get_cache_key(prompt: str) -> str:
    """Returns SHA256 hex digest of the prompt as required by Day 7 task."""
    return hashlib.sha256(prompt.encode('utf-8')).hexdigest()

def get_cached_response(prompt: str):
    if redis_client is None:
        return None
    try:
        key = get_cache_key(prompt)
        cached = redis_client.get(key)
        if cached:
            return json.loads(cached)
    except Exception as e:
        print(f"Redis get error: {e}")
    return None

def set_cached_response(prompt: str, response_data: dict, ttl_seconds: int = 900):
    """Saves to Redis with a 900s (15 minute) TTL as required."""
    if redis_client is None:
        return
    try:
        key = get_cache_key(prompt)
        redis_client.setex(key, ttl_seconds, json.dumps(response_data))
    except Exception as e:
        print(f"Redis set error: {e}")
