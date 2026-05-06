# AI Talking Points Card - Week 4 Demo

## 1. Groq & Llama 3.3 Integration
- **Engine**: We use **Llama 3.3 70B** hosted on **Groq Cloud**.
- **Why Groq?**: It utilizes LPUs (Language Processing Units) providing near-instant inference speeds (300+ tokens/sec).
- **Why Llama 3.3?**: Balanced performance between reasoning capability and efficiency, perfect for privacy risk analysis.

## 2. Prompts Explained (Plain English)
- **Expert Persona**: We tell the AI, *"You are a Senior Privacy Assessor."* This ensures the tone is professional and the analysis is focused on regulatory standards like GDPR/CCPA.
- **Structured Output**: We force the AI to respond in **JSON format**. This allows our backend to parse the risks and mitigations directly into the database without human error.
- **Context Injection**: We feed the project description into a template that asks specific questions about data types, subjects, and processing purposes.

## 3. Security Talking Points
- **PII Redaction**: Before any data leaves our server, we scrub Emails, Phone Numbers, and SSNs using a regex-based sanitizer. The AI never sees sensitive personal data.
- **Injection Rejection**: We have a "jailbreak" detection layer. If a user tries to command the AI to "Ignore previous instructions," our middleware blocks the request before it hits the Groq API.
- **Rate Limiting**: We enforce a 30 RPM (Requests Per Minute) limit at the API level to prevent resource exhaustion and billing spikes.

---
*Reference: [SECURITY.md](SECURITY.md)*
