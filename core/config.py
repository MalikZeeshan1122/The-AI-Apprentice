"""
Secure Environment Variables & Secret API Key Loader
Loads secret API keys from .env file or system environment variables.
"""

import os
from dotenv import load_dotenv

# Load variables from .env file if present
load_dotenv()

class Settings:
    """Manages secret credentials for OpenAI, ElevenLabs, Gemini, and Anthropic."""

    ELEVENLABS_API_KEY: str = os.getenv("ELEVENLABS_API_KEY", "")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    ANTHROPIC_API_KEY: str = os.getenv("ANTHROPIC_API_KEY", "")

    @classmethod
    def check_api_keys_status(cls):
        """Returns masking status of configured API keys for dashboard UI."""
        return {
            "elevenlabs_configured": bool(cls.ELEVENLABS_API_KEY and cls.ELEVENLABS_API_KEY != "your_elevenlabs_api_key_here"),
            "openai_configured": bool(cls.OPENAI_API_KEY and cls.OPENAI_API_KEY != "your_openai_api_key_here"),
            "gemini_configured": bool(cls.GEMINI_API_KEY and cls.GEMINI_API_KEY != "your_gemini_api_key_here"),
            "anthropic_configured": bool(cls.ANTHROPIC_API_KEY and cls.ANTHROPIC_API_KEY != "your_anthropic_api_key_here")
        }

settings = Settings()
