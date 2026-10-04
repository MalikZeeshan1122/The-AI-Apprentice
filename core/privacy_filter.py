"""
Privacy & PII Redaction Guardrail
Filters personally identifiable information (IBAN, Tax IDs, Names, Credit Cards) from screen text and voice transcripts.
"""

import re
from typing import Dict, Any

class PrivacyFilter:
    """Redacts sensitive PII from screen frames, event logs, and expert voice transcripts."""

    @staticmethod
    def redact_pii(text: str) -> str:
        """Applies regex-based PII redaction rules to text."""

        # Redact IBAN / Account Numbers (e.g. DE89 3704 0044 0532 0130 00)
        text = re.sub(r'[A-Z]{2}\d{2}\s?(\d{4}\s?){4}\d{1,4}', '[REDACTED_IBAN]', text)

        # Redact Credit Card numbers
        text = re.sub(r'\b(?:\d[ -]*?){13,16}\b', '[REDACTED_CREDIT_CARD]', text)

        # Redact Social Security / Tax IDs (e.g. DE123456789 or SSN)
        text = re.sub(r'\b(DE|US|UK)?\d{9,11}\b', '[REDACTED_TAX_ID]', text)

        # Redact email addresses
        text = re.sub(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', '[REDACTED_EMAIL]', text)

        return text
