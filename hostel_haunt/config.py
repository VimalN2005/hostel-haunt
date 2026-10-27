"""Configuration settings for Hostel Haunt."""

import os
from pathlib import Path

# Base Paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
RECORDINGS_DIR = DATA_DIR / "recordings"
EXPORTS_DIR = DATA_DIR / "exports"

DATA_DIR.mkdir(parents=True, exist_ok=True)
RECORDINGS_DIR.mkdir(parents=True, exist_ok=True)
EXPORTS_DIR.mkdir(parents=True, exist_ok=True)

# Database
DB_PATH = os.getenv("HOSTEL_HAUNT_DB", str(DATA_DIR / "hostel_haunt.db"))

# Model & LLM Settings
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
DEFAULT_MODEL = os.getenv("HOSTEL_HAUNT_MODEL", "gemma2:2b")
FALLBACK_MODE = os.getenv("HOSTEL_HAUNT_FALLBACK", "true").lower() in ("true", "1", "yes")

# Spooky Aesthetics Constants
APP_TITLE = "Hostel Haunt 🕯️👻"
APP_SUBTITLE = "The ghost that lives in your laptop and remembers what the night tries to forget."
