"""Streamlit user interface for the AI Resume Analyzer."""

import json
import logging
import sqlite3

import streamlit as st

from app.config.settings import Settings, SettingsError
from app.repositories.report_repository import list_reports, save_report
from app.services.resume_service import (
    ResumeAnalysis,
    ResumeAnalysisError,
    ResumeInputError,
    analyze_resume,
)
from app.utils.logging_config import configure_logging

configure_logging()
logger = logging.getLogger(__name__)

st.set_page_config(page_title="AI Resume Analyzer", page_icon="📝", layout="wide")
st.title("AI Resume Analyzer")
st.caption(
    "Get career-coaching suggestions from resume text. This prototype does not "
    "rank candidates or make hiring decisions."
)
st.warning(
    "Use fictional or consented resume data. Analysis is sent to the configured "
    "Google Gemini API and may be inaccurate or biased."
)

with st.form("resume_form"):
    resume_text = st.text_area(
        "Paste resume text",
        height=260,
        max_chars=30_000,
        help="Enter at least 50 characters. Direct identifiers are not needed.",
    )

# text

    save_to_history = st.checkbox(
        "Save this generated analysis to local history",
        value=False,
        help=(
            "Only the generated analysis is saved in a local SQLite file; "
            "the resume text is not saved."
        ),
    )
    submitted = st.form_submit_button("Analyze resume", type="primary")

if submitted:
    try:
        settings = Settings.from_env()
        analysis = analyze_resume(resume_text, settings)
        st.session_state["analysis"] = analysis.model_dump(mode="json")
        if save_to_history:
            report_id = save_report(analysis, settings.database_path)
            st.success(f"Analysis saved to local history (report {report_id}).")
        else:
            st.success("Analysis complete. The resume text was not saved.")
    except ResumeInputError as exc:
        st.error(str(exc))
    except SettingsError as exc:
        st.error(str(exc))
    except ResumeAnalysisError as exc:
        st.error(str(exc))
    except (OSError, sqlite3.Error):
        logger.exception("Could not access local report storage")
        st.error("Could not access local report storage. Check the configured path.")

analysis_data = st.session_state.get("analysis")
if analysis_data:
    analysis = ResumeAnalysis.model_validate(analysis_data)
    st.header("Analysis")
    st.subheader("Resume summary")
    st.write(analysis.summary)

    left, right = st.columns(2)
    with left:
        st.subheader("Technical skills")
        st.write(analysis.technical_skills or ["No technical skills identified."])
        st.subheader("Soft skills")
        st.write(analysis.soft_skills or ["No soft skills identified."])
        st.subheader("Experience assessment")
        st.write(analysis.experience_assessment)
        st.subheader("Potential skill gaps")
        st.write(analysis.missing_skills or ["No specific gaps identified."])
    with right:
        st.subheader("Suggested job roles")
        st.write(analysis.job_recommendations)
        st.subheader("Learning suggestions")
        st.write(analysis.learning_suggestions)
        st.subheader("Resume improvements")
        st.write(analysis.resume_improvements)

    st.download_button(
        "Download analysis as JSON",
        data=json.dumps(analysis.model_dump(mode="json"), indent=2),
        file_name="resume-analysis.json",
        mime="application/json",
    )

try:
    history_settings = Settings.from_env()
    saved_reports = list_reports(history_settings.database_path)
except (OSError, sqlite3.Error, ValueError):
    logger.exception("Could not load local report history")
    saved_reports = []
    st.error("Could not load local report history. Check the configured path.")

if saved_reports:
    with st.expander("Local analysis history"):
        st.caption("Saved analysis reports may contain personal information.")
        for report in saved_reports:
            st.markdown(
                f"**Report {report.report_id}** — "
                f"{report.created_at.strftime('%Y-%m-%d %H:%M UTC')}"
            )
            st.write(report.analysis.summary)
            st.download_button(
                "Download report",
                data=json.dumps(report.analysis.model_dump(mode="json"), indent=2),
                file_name=f"resume-analysis-{report.report_id}.json",
                mime="application/json",
                key=f"download-report-{report.report_id}",
            )
