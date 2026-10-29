"""Tests for opt-in SQLite report history."""

from pathlib import Path

import pytest

from app.repositories.report_repository import list_reports, save_report
from app.services.resume_service import ResumeAnalysis


def sample_analysis() -> ResumeAnalysis:
    return ResumeAnalysis(
        summary="A backend developer.",
        technical_skills=["Python"],
        soft_skills=["Communication"],
        experience_assessment="Relevant project experience is described.",
        job_recommendations=["Junior backend developer"],
        missing_skills=["Testing"],
        learning_suggestions=["Learn pytest"],
        resume_improvements=["Add measurable outcomes."],
    )


def test_reports_are_saved_and_listed_without_resume_text(tmp_path: Path) -> None:
    database_path = tmp_path / "nested" / "reports.sqlite3"

    report_id = save_report(sample_analysis(), database_path)
    reports = list_reports(database_path)

    assert report_id == 1
    assert len(reports) == 1
    assert reports[0].analysis == sample_analysis()
    assert reports[0].created_at.tzinfo is not None


def test_history_returns_empty_for_missing_database(tmp_path: Path) -> None:
    assert list_reports(tmp_path / "not-created.sqlite3") == []


def test_history_rejects_nonpositive_limit(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="limit must be a positive integer"):
        list_reports(tmp_path / "reports.sqlite3", limit=0)
