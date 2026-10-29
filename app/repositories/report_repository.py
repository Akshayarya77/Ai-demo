"""Opt-in local storage for generated reports; resume text is not persisted."""

from dataclasses import dataclass
from contextlib import closing
from datetime import datetime, timezone
import json
from pathlib import Path
import sqlite3

from app.services.resume_service import ResumeAnalysis


@dataclass(frozen=True)
class SavedReport:
    """A persisted analysis report."""

    report_id: int
    created_at: datetime
    analysis: ResumeAnalysis


def _connect(database_path: Path) -> sqlite3.Connection:
    database_path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(database_path)
    connection.row_factory = sqlite3.Row
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS analysis_reports (
            report_id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            report_json TEXT NOT NULL
        )
        """
    )
    return connection


def save_report(analysis: ResumeAnalysis, database_path: Path) -> int:
    """Save only the generated analysis and return its local identifier."""
    payload = json.dumps(analysis.model_dump(mode="json"), ensure_ascii=False)
    with closing(_connect(database_path)) as connection:
        with connection:
            cursor = connection.execute(
                "INSERT INTO analysis_reports (report_json) VALUES (?)", (payload,)
            )
            return int(cursor.lastrowid)


def list_reports(database_path: Path, limit: int = 20) -> list[SavedReport]:
    """Return the newest saved analyses, validating persisted JSON on read."""
    if limit < 1:
        raise ValueError("limit must be a positive integer")
    if not database_path.exists():
        return []

    with closing(_connect(database_path)) as connection:
        rows = connection.execute(
            """
            SELECT report_id, created_at, report_json
            FROM analysis_reports
            ORDER BY report_id DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()

    reports: list[SavedReport] = []
    for row in rows:
        reports.append(
            SavedReport(
                report_id=row["report_id"],
                created_at=datetime.fromisoformat(row["created_at"]).replace(
                    tzinfo=timezone.utc
                ),
                analysis=ResumeAnalysis.model_validate_json(row["report_json"]),
            )
        )
    return reports
