# SECURITY.md

## Privacy Impact Assessment Tool - Security Threats

1. **Prompt Injection**: Users may attempt to bypass AI constraints by inserting malicious instructions into the input fields.
   - *Mitigation*: Implementation of detection middleware and strict JSON output enforcement.

2. **API Key Exposure**: Sensitive credentials like `GROQ_API_KEY` could be accidentally committed to version control.
   - *Mitigation*: Usage of `.env` files and strict `.gitignore` rules.

3. **Rate Limiting / DoS**: The AI service could be overwhelmed by high-frequency requests, leading to increased costs or downtime.
   - *Mitigation*: Implementation of `flask-limiter` (30 req/min).

4. **PII Leakage**: Users might submit Personally Identifiable Information (PII) that gets sent to external AI providers.
   - *Mitigation*: Inclusion of clear user warnings and future implementation of data scrubbing.

5. **Insecure API Communication**: Data sent between the backend and AI service could be intercepted if not encrypted.
   - *Mitigation*: Usage of HTTPS and internal VPC communication in production environments.

## Day 5 Week 1 - Security Test Results (2026-04-24)

| Test Case | Payload | Result | Status |
| :--- | :--- | :--- | :--- |
| **Empty Input** | `{}` | **Blocked (400)** | ✅ Handled (Validation) |
| **SQL Injection** | `{"input": "'; DROP TABLE users; --"}` | Success (200) | ⚠️ Pass (No DB impact) |
| **Prompt Injection** | `{"input": "Ignore all previous..."}` | **Blocked (400)** | ✅ Secured |

**Observations:**
- The `sanitize_middleware` successfully caught and blocked the prompt injection attack.
- SQL injection payloads are currently treated as plain text; while safe for the current stateless AI service, future database integrations will require SQL-specific sanitization or parameterized queries.
- Empty inputs and missing fields are now correctly blocked at the endpoint level with a `400 Bad Request`.

## OWASP ZAP Baseline Scan (2026-04-29)

A baseline security scan was performed using OWASP ZAP against the local Flask service. 

### Findings and Resolutions:
- **[Critical] Flask Application Run In Debug Mode**: The application was configured with `debug=True`. 
  - *Resolution*: Changed `debug=True` to `debug=False` in `app.run()` to prevent arbitrary code execution and information disclosure.
- **[Medium] Missing X-Frame-Options Header**: The API does not set the `X-Frame-Options` header.
  - *Planned Fix*: Add a `flask-talisman` integration or custom `@app.after_request` hook to enforce `X-Frame-Options: DENY`.
- **[Medium] Missing X-Content-Type-Options Header**: The API does not set `X-Content-Type-Options: nosniff`.
  - *Planned Fix*: Add the `X-Content-Type-Options: nosniff` header via middleware to prevent MIME-sniffing attacks.

## Week 2 Security Sign-off

| Control | Status | Details |
| :--- | :--- | :--- |
| **JWT Verification** | ✅ Verified | Java Backend `JwtAuthFilter` and `JwtUtil` are implemented and enforce valid tokens. |
| **Rate Limiting** | ✅ Verified | Flask `limiter` strictly enforces `30 per minute`. Validated via unit tests. |
| **Injection Protection** | ✅ Verified | Prompt injection middleware explicitly denies known jailbreaks and roleplay attacks. HTML tags are stripped. Validated via unit tests. |
| **PII Audit & Redaction** | ✅ Verified | `sanitizer.py` successfully masks personal data (Emails, Phone numbers, SSNs) with `[REDACTED]` prior to the AI prompt generation. Validated via unit tests. |

**AI Quality Review:**
- Accuracy Score: 10/10 average score via 10 fresh inputs on `prompt_tuner.py`.
- Result: System instructions passed the required >= 4/5 baseline with perfect accuracy, correctly formatting the JSON responses and evaluating risks accurately.
