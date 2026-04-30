import requests
import time
import json

BASE_URL = "http://127.0.0.1:5000"

endpoints = [
    ("/describe", {"input": "A new healthcare app collecting patient vitals and storing them in AWS S3 with AES-256 encryption."}),
    ("/recommend", {"input": "Data retention period is set to 10 years for financial records."}),
    ("/generate-report", {"input": {"project_name": "HealthTrack", "description": "Patient monitoring system", "data_types": ["PII", "PHI"]}})
]

def run_benchmark():
    print(f"{'Endpoint':<20} | {'Status':<10} | {'Time (ms)':<10} | {'Fallback':<10}")
    print("-" * 60)
    
    total_time = 0
    total_calls = 0
    
    for path, payload in endpoints:
        start = time.time()
        try:
            resp = requests.post(f"{BASE_URL}{path}", json=payload, timeout=10)
            elapsed = (time.time() - start) * 1000
            status = resp.status_code
            data = resp.json()
            if isinstance(data, list):
                is_fallback = any(item.get("is_fallback") for item in data)
            else:
                is_fallback = data.get("is_fallback")
            
            print(f"{path:<20} | {status:<10} | {elapsed:>10.2f} | {str(is_fallback):<10}")
            
            if status == 200:
                total_time += elapsed
                total_calls += 1
        except Exception as e:
            print(f"{path:<20} | ERROR      | {'N/A':>10} | N/A ({str(e)})")

    if total_calls > 0:
        avg = total_time / total_calls
        print("-" * 60)
        print(f"Average Response Time: {avg:.2f} ms")
        if avg < 2000:
            print("PERFORMANCE TARGET MET (< 2000ms)")
        else:
            print("PERFORMANCE TARGET FAILED (> 2000ms)")

if __name__ == "__main__":
    # Check if server is running
    try:
        requests.get(BASE_URL)
        run_benchmark()
    except requests.exceptions.ConnectionError:
        print(f"Error: AI Service not running at {BASE_URL}. Please start it first.")
