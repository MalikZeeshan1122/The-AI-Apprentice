"""
Module 1: Screen Vision Event Extractor
Analyzes screen frames at 1-2 second intervals and converts screen changes into structured event streams.
"""

import time
import re
from typing import Dict, Any, List
from .privacy_filter import PrivacyFilter

class ScreenVisionExtractor:
    """Vision-capable model parser that converts screen snapshots into structured workflow events."""

    def __init__(self):
        self.privacy_filter = PrivacyFilter()

    def process_frame(self, timestamp_str: str, screen_context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parses a screen frame, extracts UI element changes, and applies PII redaction.
        """
        raw_text = screen_context.get("raw_screen_text", "")
        clean_text = self.privacy_filter.redact_pii(raw_text)

        action = screen_context.get("action", "view")
        field = screen_context.get("field", "general_screen")
        value_before = screen_context.get("value_before", "")
        value_after = screen_context.get("value_after", "")

        event = {
            "timestamp": timestamp_str,
            "invoice_id": screen_context.get("invoice_id", "INV-4471"),
            "supplier": screen_context.get("supplier", "Unassigned"),
            "amount_eur": screen_context.get("amount_eur", 0.0),
            "action_type": action,
            "field_changed": field,
            "value_before": value_before,
            "value_after": value_after,
            "clean_screen_text": clean_text,
            "event_summary": f"[{timestamp_str}] {action.upper()}: {field} changed from '{value_before}' -> '{value_after}'"
        }

        return event
