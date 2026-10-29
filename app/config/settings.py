"""Environment-backed application settings."""

from dataclasses import dataclass
import os
from pathlib import Path

from dotenv import load_dotenv


@dataclass(frozen=True)
class Settings:
    """Runtime configuration loaded from environment variables."""

    google_api_key: str
    model: str
    database_path: Path
    max_resume_chars: int = 30_000
    min_resume_chars: int = 50

    @classmethod
    def from_env(cls) -> "Settings":
        """Load settings from the environment and an optional local .env file."""
        load_dotenv()
        return cls(
            google_api_key=os.getenv("GOOGLE_API_KEY", "").strip(),
            model=os.getenv("GEMINI_MODEL", "gemini-3.8-flash").strip(),
            database_path=Path(
                os.getenv("DATABASE_PATH", "data/analysis_history.sqlite3")
            ),
        )


class SettingsError(RuntimeError):
    """Raised when required configuration is missing or invalid."""
