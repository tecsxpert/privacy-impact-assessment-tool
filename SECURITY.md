\# Security Documentation

\## Privacy Impact Assessment Tool



\*\*Team:\*\* Java Developer 2 — Bhavani R B

\*\*Date:\*\* May 8, 2026



\---



\## Threat Model



| Threat | Risk | Mitigation |

|--------|------|------------|

| SQL Injection | HIGH | JPA parameterized queries |

| XSS Attack | HIGH | Input sanitization |

| Prompt Injection | HIGH | AI input validation |

| Unauthorized Access | HIGH | JWT authentication |

| Brute Force | MEDIUM | Rate limiting 30 req/min |

| Data Exposure | MEDIUM | No PII in AI prompts |

| CSRF | MEDIUM | Spring Security CSRF |



\---



\## Security Tests Conducted



\### Test 1 — JWT Authentication

\- All endpoints require valid JWT token

\- Without token: 401 Unauthorized returned

\- Status: FIXED ✅



\### Test 2 — SQL Injection

\- Tested with: ' OR 1=1 --

\- JPA parameterized queries prevent injection

\- Status: PROTECTED ✅



\### Test 3 — Prompt Injection

\- Tested with malicious AI inputs

\- Input sanitization middleware blocks attacks

\- Status: PROTECTED ✅



\### Test 4 — Rate Limiting

\- Flask limiter: 30 requests per minute

\- Exceeding limit returns 429 Too Many Requests

\- Status: IMPLEMENTED ✅



\### Test 5 — File Upload Security

\- Only PDF and DOCX allowed

\- Maximum file size: 5MB

\- Content-Type validation enforced

\- Status: PROTECTED ✅



\---



\## Findings Fixed



| Finding | Severity | Status |

|---------|----------|--------|

| Hardcoded secrets | CRITICAL | FIXED |

| Missing JWT on endpoints | HIGH | FIXED |

| No file type validation | HIGH | FIXED |

| No rate limiting | MEDIUM | FIXED |



\---



\## Residual Risks



| Risk | Level | Reason |

|------|-------|--------|

| Docker misconfiguration | LOW | Dev environment only |

| Redis no auth | LOW | Internal network only |



\---



\## Sign Off

\- Java Developer 2: Bhavani R B ✅

\- Date: May 8, 2026

