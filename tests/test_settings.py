"""Tests for environment-backed settings."""

from pathlib import Path

from app.config.settings import Settings


def test_settings_use_environment_values(monkeypatch) -> None:
    monkeypatch.setenv("GOOGLE_API_KEY", " test-key ")
    monkeypatch.setenv("GEMINI_MODEL", "test-model")
    monkeypatch.setenv("DATABASE_PATH", "tmp/reports.sqlite3")

    settings = Settings.from_env()

    assert settings.google_api_key == "test-key"
    assert settings.model == "test-model"
    assert settings.database_path == Path("tmp/reports.sqlite3")


def test_settings_have_safe_defaults_when_key_is_missing(monkeypatch) -> None:
    monkeypatch.delenv("GOOGLE_API_KEY", raising=False)
    monkeypatch.delenv("GEMINI_MODEL", raising=False)
    monkeypatch.delenv("DATABASE_PATH", raising=False)

    settings = Settings.from_env()

    assert settings.google_api_key == ""
    assert settings.model == "gemini-3.8-flash"
    assert settings.database_path == Path("data/analysis_history.sqlite3")
