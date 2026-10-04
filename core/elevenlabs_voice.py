"""
ElevenLabs Voice Agent & Pause Detector Integration
Manages natural pause detection, real-time voice prompts, and ElevenLabs API audio generation.
"""

import time
import random
import logging
from typing import Dict, Any, List
from core.config import settings

logger = logging.getLogger(__name__)

class ElevenLabsVoiceCompanion:
    """ElevenLabs Conversational Voice Agent integration with natural pause detection and Expressive voice synthesis."""

    def __init__(self, voice_id: str = "21m00Tcm4TlvDq8ikWAM", agent_name: str = "Apprentice Companion"):
        self.voice_id = voice_id
        self.agent_name = agent_name
        self.api_key = settings.ELEVENLABS_API_KEY
        self.conversation_transcript = []
        self.client = None

        # Initialize official ElevenLabs SDK client if API key is provided
        if self.api_key and self.api_key != "your_elevenlabs_api_key_here":
            try:
                from elevenlabs.client import ElevenLabs
                self.client = ElevenLabs(api_key=self.api_key)
                logger.info("ElevenLabs SDK client initialized successfully!")
            except Exception as e:
                logger.warning(f"Could not initialize ElevenLabs client: {e}")

    def generate_voice_audio(self, text: str) -> Dict[str, Any]:
        """
        Calls ElevenLabs API to synthesize expressive voice audio for spoken prompts.
        """
        if self.client:
            try:
                # Call ElevenLabs API to generate audio
                audio = self.client.generate(
                    text=text,
                    voice=self.voice_id,
                    model="eleven_multilingual_v2"
                )
                return {"status": "SUCCESS", "audio_generated": True, "voice_id": self.voice_id}
            except Exception as e:
                logger.warning(f"ElevenLabs live API call error: {e}")
                return {"status": "API_ERROR", "error": str(e)}
        
        return {
            "status": "SIMULATED",
            "message": "Add ELEVENLABS_API_KEY to .env to enable live voice synthesis.",
            "voice_id": self.voice_id
        }

    def detect_pause_and_prompt(self, current_event: Dict[str, Any], is_typing: bool = False) -> Dict[str, Any]:
        """
        Determines if the expert has reached a natural pause, then selects a targeted question.
        Required: Asks at least 3 live questions per session, including at least 1 about a guardrail.
        """
        if is_typing:
            return {"asked": False, "reason": "Expert is actively typing. Voice agent stays quiet."}

        action = current_event.get("action_type", "")
        amount = current_event.get("amount_eur", 0.0)
        field = current_event.get("field_changed", "")
        supplier = current_event.get("supplier", "")

        question_text = None
        question_category = "General"

        # Question Rule 1: Guardrail Check for High Amount / CapEx
        if amount > 5000 and "cost_center" in field:
            question_text = f"Sabine, I noticed you moved Invoice #{current_event.get('invoice_id')} (€{amount:,.2f}) to Cost Center {current_event.get('value_after')}. What rule made you choose that code?"
            question_category = "Guardrail: CapEx Threshold"

        # Question Rule 2: Exception Check for Specific Supplier (e.g. December Double Billing)
        elif "hold" in action or "double" in supplier.lower() or "december" in field.lower():
            question_text = f"You put a hold on the invoice for {supplier}. Is that true for every December invoice, and who decides when to release it?"
            question_category = "Guardrail: Supplier Exception"

        # Question Rule 3: Cross-Border / Subsidiary Approval
        elif "czech" in supplier.lower() or "approval" in field:
            question_text = f"This invoice comes from the Czech subsidiary. What is the limit before a second approval is required?"
            question_category = "Guardrail: Approval Hierarchy"

        # Default pause question
        else:
            question_text = f"You changed {field} to {current_event.get('value_after')}. What would happen if a new hire left it as {current_event.get('value_before')}?"
            question_category = "Decision Rationale"

        transcript_entry = {
            "timestamp": current_event.get("timestamp", "03:15"),
            "agent_speaker": "ElevenLabs Voice Companion (Expressive Mode)",
            "question": question_text,
            "category": question_category,
            "screen_event_ref": current_event.get("event_summary")
        }
        self.conversation_transcript.append(transcript_entry)

        # Generate audio status via ElevenLabs
        audio_status = self.generate_voice_audio(question_text)

        return {
            "asked": True,
            "question": question_text,
            "category": question_category,
            "audio_voice_id": self.voice_id,
            "expressive_mode": "Curious & Patient",
            "elevenlabs_status": audio_status
        }
