import requests
import json
import time
import os

BASE_URL = "http://127.0.0.1:5000"
RECORDS_FILE = "c:/Users/HP/Desktop/privacy-impact-assessment-tool/ai-service/scratch/demo_records.json"
RESULTS_FILE = "c:/Users/HP/Desktop/privacy-impact-assessment-tool/ai-service/scratch/demo_results.json"

def run_demo():
    print("Starting demo run for 30 records...")
    
    with open(RECORDS_FILE, "r") as f:
        records = json.load(f)
    
    results = []
    
    for i, record in enumerate(records):
        print(f"Processing record {i+1}/30: {record[:50]}...")
        
        # We alternate between endpoints to test all prompts
        if i % 3 == 0:
            endpoint = "/describe"
        elif i % 3 == 1:
            endpoint = "/recommend"
        else:
            endpoint = "/generate-report"
            
        start_time = time.time()
        try:
            resp = requests.post(f"{BASE_URL}{endpoint}", json={"input": record}, timeout=15)
            elapsed = time.time() - start_time
            
            if resp.status_code == 200:
                data = resp.json()
                results.append({
                    "id": i + 1,
                    "input": record,
                    "endpoint": endpoint,
                    "output": data,
                    "time_ms": round(elapsed * 1000, 2)
                })
            else:
                print(f"Failed to process record {i+1}: {resp.status_code}")
        except Exception as e:
            print(f"Error processing record {i+1}: {e}")
            
    with open(RESULTS_FILE, "w") as f:
        json.dump(results, f, indent=2)
        
    print(f"Demo run complete. Results saved to {RESULTS_FILE}")

if __name__ == "__main__":
    # Check if server is running
    try:
        requests.get(BASE_URL)
        run_demo()
    except requests.exceptions.ConnectionError:
        print(f"Error: AI Service not running at {BASE_URL}. Please start it first.")
