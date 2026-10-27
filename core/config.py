"""Shared, environment-overridable SafeSignal settings."""

import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
MAX_MESSAGE_LENGTH = 20_000
DEFAULT_LANGUAGE = "fr"
SUPPORTED_LANGUAGES = ("fr", "en", "ar")
DEFAULT_DB_PATH = PROJECT_ROOT / "db" / "safesignal.sqlite3"
DB_PATH = Path(os.environ.get("SAFESIGNAL_DB_PATH", str(DEFAULT_DB_PATH))).expanduser()
