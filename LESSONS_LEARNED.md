# Post-Demo: Lessons Learned & Future Sprints

## 1. Lessons Learned
- **Containerization Complexity**: Managing dependencies across Python (Flask), Java (Spring Boot), and PostgreSQL in Docker requires precise health checks and network orchestration.
- **AI Response Consistency**: Prompt engineering is critical. Using system-level persona instructions significantly improved the reliability of JSON outputs compared to user-level instructions.
- **Security First**: Implementing PII redaction *before* the data reaches the external AI provider is a non-negotiable requirement for privacy-focused tools.

## 2. Features for Future Sprints
- **Automated PIA Review Workflow**: Implementing a multi-stage approval process where senior DPOs can review AI-generated assessments.
- **Support for Multi-Regional Compliance**: Adding specific prompt layers for HIPAA (US), CCPA (California), and LGPD (Brazil).
- **Fine-Tuning**: Moving from general-purpose Llama 3 to a fine-tuned model trained specifically on privacy case law and regulatory documents.
- **Interactive Risk Dashboard**: A visual heat-map of privacy risks across all company projects.

## 3. Mentor Feedback (Placeholder)
- *To be filled after Demo Day feedback session.*
- [ ] Incorporate suggestions on risk scoring algorithm.
- [ ] Review UI accessibility for color-blind users (specifically the risk badges).

---
*Completed Week 4 Deliverables*
