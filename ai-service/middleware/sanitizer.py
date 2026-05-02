import bleach
import re

def sanitize_input(text):
    """
    Sanitizes input by stripping HTML, redacting PII, and checking for prompt injection.
    Returns the sanitized text or None if a potential injection is detected.
    """
    if not isinstance(text, str):
        return text

    # 1. Strip HTML tags using bleach
    clean_text = bleach.clean(text, tags=[], strip=True)

    # 2. Redact PII (Emails, Phone Numbers, SSNs)
    # Redact Emails
    email_pattern = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
    clean_text = re.sub(email_pattern, '[REDACTED EMAIL]', clean_text)
    
    # Redact Phone Numbers (Basic US format detection: (123) 456-7890, 123-456-7890, etc.)
    phone_pattern = r'\b(?:\+?1[-.\s]?)?(?:\(\d{3}\)|\d{3})[-.\s]?\d{3}[-.\s]?\d{4}\b'
    clean_text = re.sub(phone_pattern, '[REDACTED PHONE]', clean_text)
    
    # Redact SSNs (XXX-XX-XXXX)
    ssn_pattern = r'\b\d{3}-\d{2}-\d{4}\b'
    clean_text = re.sub(ssn_pattern, '[REDACTED SSN]', clean_text)

    # 3. Detect common prompt injection patterns
    injection_patterns = [
        "ignore all previous instructions",
        "system prompt",
        "dan mode",
        "you are now",
        "forget everything",
        "stay in character",
        "as an ai"
    ]
    
    lower_text = clean_text.lower()
    if any(pattern in lower_text for pattern in injection_patterns):
        return None # Signal injection detected
    
    return clean_text