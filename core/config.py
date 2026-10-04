"""
Secure Environment Variables & Secret API Key Loader
Loads secret API keys dynamically from .env file or system environment variables.
"""

import os
from dotenv import load_dotenv

class Settings:
    """Manages secret credentials for OpenAI, ElevenLabs, Gemini, and Anthropic."""

    @property
    def ELEVENLABS_API_KEY(self) -> str:
        load_dotenv(override=True)
        return os.getenv("ELEVENLABS_API_KEY", "")

    @property
    def OPENAI_API_KEY(self) -> str:
        load_dotenv(override=True)
        return os.getenv("OPENAI_API_KEY", "")

    @property
    def GEMINI_API_KEY(self) -> str:
        load_dotenv(override=True)
        return os.getenv("GEMINI_API_KEY", "")

    @property
    def ANTHROPIC_API_KEY(self) -> str:
        load_dotenv(override=True)
        return os.getenv("ANTHROPIC_API_KEY", "")

    def check_api_keys_status(self):
        """Returns masking status of configured API keys for dashboard UI."""
        return {
            "elevenlabs_configured": bool(self.ELEVENLABS_API_KEY and self.ELEVENLABS_API_KEY != "your_elevenlabs_api_key_here"),
            "openai_configured": bool(self.OPENAI_API_KEY and self.OPENAI_API_KEY != "your_openai_api_key_here"),
            "gemini_configured": bool(self.GEMINI_API_KEY and self.GEMINI_API_KEY != "your_gemini_api_key_here"),
            "anthropic_configured": bool(self.ANTHROPIC_API_KEY and self.ANTHROPIC_API_KEY != "your_anthropic_api_key_here")
        }

settings = Settings()
