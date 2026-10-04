"""
The AI Apprentice: FastAPI REST Server
Provides HTTP API endpoints for Screen Vision Capture, ElevenLabs Voice Prompts, Work Map Generation, and Voice Tutor Interceptor.
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
import uvicorn
import json
import os
import sys

# Ensure core imports work
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.screen_vision import ScreenVisionExtractor
from core.elevenlabs_voice import ElevenLabsVoiceCompanion
from core.work_map_generator import WorkMapGenerator
from core.voice_tutor import VoiceTutorCoach
from core.privacy_filter import PrivacyFilter

app = FastAPI(
    title="The AI Apprentice REST API",
    description="ElevenLabs × Hack-Nation 7th Global AI Hackathon API Backend",
    version="1.0.0"
)

# Enable CORS for Web Extensions & Frontends
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global Instances
vision_extractor = ScreenVisionExtractor()
voice_companion = ElevenLabsVoiceCompanion()
work_map_generator = WorkMapGenerator()

# -----------------------------------------------------------------------------
# PYDANTIC SCHEMAS
# -----------------------------------------------------------------------------
class FrameCaptureRequest(BaseModel):
    timestamp: str = Field(default="03:12", description="Timestamp string MM:SS")
    invoice_id: str = Field(default="INV-4471", description="Current invoice ID on screen")
    supplier: str = Field(default="Stuttgart CNC Components GmbH", description="Supplier name")
    amount_eur: float = Field(default=7200.0, description="Invoice amount in EUR")
    action_type: str = Field(default="recoded_cost_center", description="Action type on screen")
    field_changed: str = Field(default="cost_center", description="UI field modified")
    value_before: str = Field(default="4711 (OpEx)", description="Previous field value")
    value_after: str = Field(default="0400 (CapEx)", description="New field value")
    raw_screen_text: Optional[str] = Field(default="", description="Raw OCR or screen text")
    is_typing: bool = Field(default=False, description="Whether expert is actively typing")

class NewHireActionRequest(BaseModel):
    amount_eur: float = Field(default=7500.0, description="Invoice amount in EUR")
    cost_center_selected: str = Field(default="4711 (OpEx)", description="Cost center selected by new hire")
    supplier: str = Field(default="Industrial Equipment Direct", description="Supplier name")
    has_asset_tag: bool = Field(default=True, description="Whether asset tag number is attached")

# -----------------------------------------------------------------------------
# API ENDPOINTS
# -----------------------------------------------------------------------------
@app.get("/")
def root():
    """Root Endpoint - API Status & Meta Information."""
    return {
        "status": "ONLINE",
        "service": "The AI Apprentice Backend Engine",
        "hackathon": "7th Global AI Hackathon · ElevenLabs × Hack-Nation",
        "documentation": "/docs"
    }

@app.post("/api/v1/capture/frame")
def process_screen_frame(req: FrameCaptureRequest):
    """
    Module 1: Processes a screen frame snapshot, redacts PII, and returns ElevenLabs Voice Companion prompt.
    """
    screen_ctx = {
        "invoice_id": req.invoice_id,
        "supplier": req.supplier,
        "amount_eur": req.amount_eur,
        "action": req.action_type,
        "field": req.field_changed,
        "value_before": req.value_before,
        "value_after": req.value_after,
        "raw_screen_text": req.raw_screen_text
    }

    event = vision_extractor.process_frame(req.timestamp, screen_ctx)
    voice_prompt = voice_companion.detect_pause_and_prompt(event, is_typing=req.is_typing)

    return {
        "processed_event": event,
        "voice_companion_response": voice_prompt
    }

@app.get("/api/v1/work-map")
def get_work_map():
    """
    Module 2: Generates and returns the complete, clickable Work Map JSON.
    """
    work_map = work_map_generator.generate_work_map([], [])
    return work_map

@app.post("/api/v1/tutor/evaluate")
def evaluate_new_hire_action(req: NewHireActionRequest):
    """
    Module 3: Evaluates a new hire's screen action in real-time.
    Intercepts mistakes before they are saved and returns expert quotes & screen moments.
    """
    work_map = work_map_generator.generate_work_map([], [])
    tutor = VoiceTutorCoach(work_map)

    action = {
        "amount_eur": req.amount_eur,
        "cost_center_selected": req.cost_center_selected,
        "supplier": req.supplier,
        "has_asset_tag": req.has_asset_tag
    }

    result = tutor.evaluate_new_hire_action(action)
    mastery = tutor.get_mastery_report()

    return {
        "interception_result": result,
        "trainee_mastery_report": mastery
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
