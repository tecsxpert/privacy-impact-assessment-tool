import bleach
import re

def sanitize_input(text):
    """
    Sanitizes input by stripping HTML and checking for prompt injection patterns.
    Returns the sanitized text or None if a potential injection is detected.
    """
    if not isinstance(text, str):
        return text

    # 1. Strip HTML tags using bleach
    clean_text = bleach.clean(text, tags=[], strip=True)

    # 2. Detect common prompt injection patterns
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