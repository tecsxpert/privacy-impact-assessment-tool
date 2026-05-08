# AI Summary Card: Privacy Impact Assessment Tool

## Project Overview
A secure, AI-powered tool designed to automate Privacy Impact Assessments (PIA) while maintaining strict data privacy and security standards.

## Core AI Endpoints
1. **POST `/analyze`**: Performs deep privacy risk analysis on project descriptions. Returns structured JSON risks and mitigations.
2. **GET `/health`**: Real-time status monitoring of the AI inference engine.
3. **POST `/validate`**: (Internal) Security middleware validation for prompt injection and PII detection.

## Technical Stack
- **AI Inference**: Llama 3.3 (70B) via Groq Cloud API.
- **Backend**: Spring Boot 3.2 (Java 17), PostgreSQL, Redis.
- **AI Service**: Flask (Python 3.11), `flask-limiter`, `bleach`.
- **Frontend**: React + Vite, Tailwind CSS.
- **Infrastructure**: Docker, Docker Compose.

## Key Security Features
- **PII Redaction**: Automated masking of emails, phones, and SSNs.
- **Injection Defense**: Regex and heuristic-based prompt injection blocking.
- **Rate Limiting**: Tiered limiting to prevent API abuse (30 RPM).

## GitHub Repository
[https://github.com/Veeresh-hp/privacy-impact-assessment-tool](https://github.com/Veeresh-hp/privacy-impact-assessment-tool)

---
*Printed for Demo Day - Week 3 Final Deliverable*
