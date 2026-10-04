"""
API Keys Live Connectivity Tester
Tests live authentication for ElevenLabs API and OpenAI API keys.
"""

import os
import sys
import requests
from core.config import settings

# Force stdout UTF-8 encoding for Windows terminal
sys.stdout.reconfigure(encoding='utf-8')

def test_elevenlabs():
    key = settings.ELEVENLABS_API_KEY
    if not key or key == "your_elevenlabs_api_key_here":
        return "[FAIL] ELEVENLABS_API_KEY is missing."

    # Test Voices endpoint
    url = "https://api.elevenlabs.io/v1/voices"
    headers = {"xi-api-key": key}
    try:
        res = requests.get(url, headers=headers, timeout=10)
        if res.status_code == 200:
            voices = res.json().get("voices", [])
            return f"[SUCCESS] ElevenLabs API Key is WORKING! Total available voices: {len(voices)}"
        else:
            return f"[FAIL] ElevenLabs API Key Permission Notice (Status {res.status_code}): {res.text}"
    except Exception as e:
        return f"[FAIL] ElevenLabs Connection Error: {e}"

def test_openai():
    key = settings.OPENAI_API_KEY
    if not key or key == "your_openai_api_key_here":
        return "[FAIL] OPENAI_API_KEY is missing."

    url = "https://api.openai.com/v1/models"
    headers = {"Authorization": f"Bearer {key}"}
    try:
        res = requests.get(url, headers=headers, timeout=10)
        if res.status_code == 200:
            models = res.json().get("data", [])
            return f"[SUCCESS] OpenAI API Key is WORKING! Total available models: {len(models)}"
        else:
            return f"[FAIL] OpenAI API Error {res.status_code}: {res.text}"
    except Exception as e:
        return f"[FAIL] OpenAI Connection Error: {e}"

if __name__ == "__main__":
    print("=" * 70)
    print("  TESTING LIVE API KEYS AUTHENTICATION")
    print("=" * 70)
    print(test_elevenlabs())
    print(test_openai())
    print("=" * 70)
