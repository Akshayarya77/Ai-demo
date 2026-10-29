"""Resume input validation and Gemini-backed analysis."""

import logging

from google.api_core.exceptions import GoogleAPIError
from google.genai.errors import APIError as GeminiAPIError
from langchain_core.exceptions import OutputParserException
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel, ConfigDict, ValidationError

from app.config.settings import Settings, SettingsError
from app.prompts.resume_prompt import SYSTEM_PROMPT

logger = logging.getLogger(__name__)


class ResumeInputError(ValueError):
    """Raised when resume text does not meet input requirements."""


class ResumeAnalysisError(RuntimeError):
    """Raised when the model call fails or returns invalid structured output."""


class ResumeAnalysis(BaseModel):
    """Validated result fields displayed by the application."""

    model_config = ConfigDict(extra="forbid")

    summary: str
    technical_skills: list[str]
    soft_skills: list[str]
    experience_assessment: str
    job_recommendations: list[str]
    missing_skills: list[str]
    learning_suggestions: list[str]
    resume_improvements: list[str]


def validate_resume_text(
    resume_text: str, min_chars: int = 50, max_chars: int = 30_000
) -> str:
    """Normalize and validate resume text before sending it to the API."""
    normalized = resume_text.strip()
    if len(normalized) < min_chars:
        raise ResumeInputError(
            f"Enter at least {min_chars} characters of resume text."
        )
    if len(normalized) > max_chars:
        raise ResumeInputError(
            f"Resume text must be no more than {max_chars:,} characters."
        )
    return normalized


def analyze_resume(
    resume_text: str,
    settings: Settings,
) -> ResumeAnalysis:
    """Analyze resume text and validate the model's response."""
    normalized = validate_resume_text(
        resume_text,
        min_chars=settings.min_resume_chars,
        max_chars=settings.max_resume_chars,
    )
    if not settings.google_api_key:
        raise SettingsError(
            "Set GOOGLE_API_KEY in your environment or local .env file."
        )

    try:
        model = ChatGoogleGenerativeAI(
            model=settings.model,
            google_api_key=settings.google_api_key,
            temperature=0.2,
        )
        structured_model = model.with_structured_output(ResumeAnalysis)
        result = structured_model.invoke(
            [
                ("system", SYSTEM_PROMPT),
                (
                    "human",
                    "Analyze the following resume text.\n\n"
                    f"<resume>\n{normalized}\n</resume>",
                ),
            ]
        )
    except (GeminiAPIError, GoogleAPIError) as exc:
        logger.error("Gemini resume analysis failed (%s)", type(exc).__name__)
        raise ResumeAnalysisError(
            "The analysis service could not complete the request. "
            "Check the API configuration and try again."
        ) from exc
    except (OutputParserException, ValidationError) as exc:
        logger.warning("Gemini returned invalid structured output")
        raise ResumeAnalysisError(
            "The analysis service returned an invalid result. Please try again."
        ) from exc

    if isinstance(result, ResumeAnalysis):
        return result
    try:
        return ResumeAnalysis.model_validate(result)
    except (ValidationError, ValueError, TypeError) as exc:
        logger.warning("Gemini returned invalid structured output")
        raise ResumeAnalysisError(
            "The analysis service returned an invalid result. Please try again."
        ) from exc
