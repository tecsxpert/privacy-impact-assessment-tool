import os
import time
import requests
import json
import logging
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

class GroqClient:
    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")
        self.url = "https://api.groq.com/openai/v1/chat/completions"

    def call_ai(self, prompt, model="llama-3.1-8b-instant", temperature=0.3, max_retries=3):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": temperature,
            "response_format": {"type": "json_object"}
        }

        for attempt in range(max_retries):
            try:
                response = requests.post(self.url, headers=headers, json=payload, timeout=30)
                if response.status_code == 200:
                    return response.json()
                elif response.status_code == 429:
                    logger.warning(f"Rate limit hit. Attempt {attempt + 1}")
                else:
                    logger.error(f"API Error {response.status_code}: {response.text}")
            except Exception as e:
                logger.error(f"Connection failed: {str(e)}")
            
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt) # Exponential backoff
        
        return None

groq_client = GroqClient()
