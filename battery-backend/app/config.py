"""
Central place for environment variables / settings.
Everyone on the team imports from here instead of calling os.getenv()
directly all over the codebase - keeps things consistent.
"""

import os
from dotenv import load_dotenv

# Load variables from a local .env file (if present).
load_dotenv()

class Settings:
    DATABASE_URL: str = os.getenv("DATABASE_URL", "")
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    ALLOWED_ORIGINS: str = os.getenv("ALLOWED_ORIGINS", "*")

    # Path to the shared telemetry CSV - every router reads from this same file
    TELEMETRY_CSV_PATH: str = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "app", "data", "vehicles_telemetry.csv"
    )

settings = Settings()
