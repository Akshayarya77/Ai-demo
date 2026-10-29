"""Tests for resume validation and model response parsing."""

from pathlib import Path
from unittest.mock import Mock

from google.genai.errors import APIError as GeminiAPIError
import pytest

from app.config.settings import Settings, SettingsError
from app.services.resume_service import (
    ResumeAnalysis,
    ResumeAnalysisError,
    ResumeInputError,
    analyze_resume,
    validate_resume_text,
)


def valid_payload() -> dict[str, object]:
    return {
        "summary": "A backend developer with API experience.",
        "technical_skills": ["Python", "REST APIs"],
        "soft_skills": ["Collaboration"],
        "experience_assessment": "The resume describes two years of experience.",
        "job_recommendations": ["Junior backend developer"],
        "missing_skills": ["Automated testing"],
        "learning_suggestions": ["Practice pytest"],
        "resume_improvements": ["Add measurable outcomes to project bullets."],
    }


def test_validate_resume_text_strips_whitespace() -> None:
    assert validate_resume_text("  " + "A" * 50 + "  ") == "A" * 50


@pytest.mark.parametrize(
    "resume_text",
    ["", "too short"],
)
def test_validate_resume_text_rejects_short_input(resume_text: str) -> None:
    with pytest.raises(ResumeInputError):
        validate_resume_text(resume_text)


def test_validate_resume_text_rejects_oversized_input() -> None:
    with pytest.raises(ResumeInputError, match="no more than"):
        validate_resume_text("A" * 51, min_chars=1, max_chars=50)


def test_analyze_resume_parses_valid_response_without_network(monkeypatch) -> None:
    structured_model = Mock()
    structured_model.invoke.return_value = valid_payload()
    model = Mock()
    model.with_structured_output.return_value = structured_model
    model_factory = Mock(return_value=model)
    monkeypatch.setattr(
        "app.services.resume_service.ChatGoogleGenerativeAI", model_factory
    )
    settings = Settings(
        google_api_key="test-key",
        model="test-model",
        database_path=Path("unused.sqlite3"),
    )

    result = analyze_resume("A" * 50, settings)

    assert result.summary == "A backend developer with API experience."
    model_factory.assert_called_once_with(
        model="test-model",
        google_api_key="test-key",
        temperature=0.2,
    )
    model.with_structured_output.assert_called_once_with(ResumeAnalysis)
    structured_model.invoke.assert_called_once()


def test_analyze_resume_requires_api_key_before_calling_model(monkeypatch) -> None:
    model_factory = Mock()
    monkeypatch.setattr(
        "app.services.resume_service.ChatGoogleGenerativeAI", model_factory
    )
    settings = Settings(
        google_api_key="",
        model="test-model",
        database_path=Path("unused.sqlite3"),
    )

    with pytest.raises(SettingsError, match="GOOGLE_API_KEY"):
        analyze_resume("A" * 50, settings)
    model_factory.assert_not_called()


def test_analyze_resume_rejects_invalid_model_output(monkeypatch) -> None:
    structured_model = Mock()
    structured_model.invoke.return_value = {"summary": "x"}
    model = Mock()
    model.with_structured_output.return_value = structured_model
    monkeypatch.setattr(
        "app.services.resume_service.ChatGoogleGenerativeAI",
        Mock(return_value=model),
    )
    settings = Settings(
        google_api_key="test-key",
        model="test-model",
        database_path=Path("unused.sqlite3"),
    )

    with pytest.raises(ResumeAnalysisError, match="invalid result"):
        analyze_resume("A" * 50, settings)


def test_analyze_resume_translates_google_api_error(monkeypatch) -> None:
    structured_model = Mock()
    structured_model.invoke.side_effect = GeminiAPIError(
        503, {"message": "service unavailable"}
    )
    model = Mock()
    model.with_structured_output.return_value = structured_model
    monkeypatch.setattr(
        "app.services.resume_service.ChatGoogleGenerativeAI",
        Mock(return_value=model),
    )
    settings = Settings(
        google_api_key="test-key",
        model="test-model",
        database_path=Path("unused.sqlite3"),
    )

    with pytest.raises(ResumeAnalysisError, match="could not complete"):
        analyze_resume("A" * 50, settings)
