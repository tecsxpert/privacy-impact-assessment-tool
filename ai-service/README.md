# Privacy Impact Assessment AI Service

This microservice provides AI-powered analysis and recommendations for Privacy Impact Assessments (PIA) using the Groq API and Llama 3.1 models.

## Features
- **Project Description Generation**: Summarizes project goals and data collection practices.
- **Risk Recommendations**: Provides actionable privacy risk mitigation strategies.
- **Full Report Generation**: Generates structured JSON reports for privacy assessments.
- **Performance Optimized**: Sub-2s response times using `llama-3.1-8b-instant`.
- **Robustness**: Automated fallback mechanisms when AI services are unavailable.
- **Security**: Input sanitization, rate limiting, and secure headers (OWASP aligned).

## Prerequisites
- Python 3.10+
- Redis (for caching, optional but recommended)
- Groq API Key

## Setup

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Environment Variables**:
   Create a `.env` file in the `ai-service/` directory:
   ```env
   GROQ_API_KEY=your_groq_api_key_here
   REDIS_URL=redis://localhost:6379/0
   ```

## Running the Service

Start the Flask application:
```bash
python app.py
```
The service will be available at `http://127.0.0.1:5000`.

---

## API Reference

### 1. Describe Project
Analyzes raw project input and generates a structured summary with identified data types and risk levels.

- **Endpoint**: `POST /describe`
- **Request Body**:
  ```json
  {
    "input": "We are building a fitness app that tracks user location and heart rate using wearable devices."
  }
  ```
- **Example Response**:
  ```json
  {
    "summary": "Health tracking application collecting biometric and geolocation data.",
    "data_collected": ["Location", "Heart Rate", "User Identity"],
    "privacy_risks": ["Continuous tracking of sensitive health data"],
    "risk_level": "High",
    "generated_at": "2026-04-30T15:00:00Z"
  }
  ```

### 2. Get Recommendations
Provides specific privacy recommendations based on the project description or data handling practices.

- **Endpoint**: `POST /recommend`
- **Request Body**:
  ```json
  {
    "input": "User data is stored in a plain text file on a public cloud bucket."
  }
  ```
- **Example Response**:
  ```json
  [
    {
      "action_type": "Encryption",
      "description": "Implement AES-256 encryption for data at rest.",
      "priority": "Critical"
    },
    {
      "action_type": "Access Control",
      "description": "Restrict bucket access to authorized service accounts only.",
      "priority": "High"
    }
  ]
  ```

### 3. Generate Full Report
Generates a comprehensive structured report suitable for a final Privacy Impact Assessment document.

- **Endpoint**: `POST /generate-report`
- **Request Body**:
  ```json
  {
    "input": {
      "project_name": "HealthTrack",
      "data_types": ["PII", "Biometrics"],
      "retention": "5 years"
    }
  }
  ```
- **Example Response**:
  ```json
  {
    "title": "Privacy Impact Assessment: HealthTrack",
    "summary": "Comprehensive analysis of biometric data handling.",
    "overview": "Detailed breakdown of risks associated with 5-year data retention.",
    "key_items": ["Biometric encryption", "Retention policy compliance"],
    "recommendations": ["Reduce retention to 2 years", "Anonymize data"],
    "status": "success",
    "generated_at": "2026-04-30T15:00:00Z"
  }
  ```

---

## Performance and Monitoring
- **Health Check**: `GET /health` returns service uptime and average response times.
- **Caching**: AI responses are cached in Redis for 15 minutes to reduce API costs and latency.
- **Optimization**: Uses `llama-3.1-8b-instant` for ultra-fast processing (< 2s average).
