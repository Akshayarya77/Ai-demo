# AI Resume Analyzer

A Streamlit demo that turns pasted resume text into a structured analysis using LangChain and Google's Gemini API. It produces a summary, skills assessment, experience review, job-role suggestions, skill gaps, learning suggestions, and resume improvements.

> **Limitations:** This is a workshop prototype, not a hiring or screening system. Its output can be incomplete or incorrect and must not be used to make employment decisions. Do not submit sensitive information unless you have permission to process it.

## Features

- Paste resume text into the browser; no resume-file upload is required.
- Generate typed, structured recommendations using a Gemini chat model through LangChain.
- Download the result as JSON.
- Optionally save an analysis to a local SQLite history. Raw resume text is never stored. Saved analysis can still contain personal information, so saving is off by default.
- Unit tests use mocked API responses and do not need an API key or internet access.

## Project structure

```text
app/
  config/settings.py              Environment-backed configuration
  prompts/resume_prompt.py        Analysis instructions for the model
  repositories/report_repository.py Local SQLite report history
  services/resume_service.py      Input validation and LangChain/Gemini integration
  utils/logging_config.py         Application logging
  main.py                         Streamlit user interface
tests/
  test_report_repository.py
  test_resume_service.py
  test_settings.py
```

## Requirements

- Python 3.10 or newer
- A Google AI API key for live Gemini analysis

## Install and configure

### Windows (PowerShell)

```powershell
cd D:\path\to\Ai-demo
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
notepad .env
```

### Linux / macOS

```bash
cd /path/to/Ai-demo
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
cp .env.example .env
${EDITOR:-nano} .env
```

Set `GOOGLE_API_KEY` in `.env`. The default model is `gemini-3.8-flash`; change `GEMINI_MODEL` if your Google AI account supports another Gemini model. Never commit `.env`.

## Run

```bash
streamlit run app/main.py
```

Streamlit prints a local URL to open in your browser. Paste resume text and select **Analyze resume**. The application validates a minimum and maximum input length before making an API request.

## Run tests

```bash
python -m pytest
```

Tests are deterministic and mock the LangChain Gemini model boundary. They do not make API calls.

## Configuration

| Variable | Required | Default | Purpose |
|---|---:|---|---|
| `GOOGLE_API_KEY` | For analysis | — | Google AI API credential; keep it private |
| `GEMINI_MODEL` | No | `gemini-3.8-flash` | Gemini model name |
| `DATABASE_PATH` | No | `data/analysis_history.sqlite3` | Local path for opt-in saved reports |

## Privacy and security

- Resume contents are sent to the configured Google Gemini API through LangChain only when the user submits an analysis; review Google's terms and data controls before using real personal data.
- The app does not save raw resume text. If the user checks the save-history option, the generated analysis is written to a local SQLite file and may itself contain personal information.
- Keep `.env` and local database files out of source control. The sample `.gitignore` excludes both.
- The demo logs operational errors without logging resume contents or API credentials.
- Generated recommendations may be biased, stale, or fabricated. Review them with a qualified career counselor; do not use this application for automated hiring decisions.

## Troubleshooting

- **Missing API key:** Put a valid `GOOGLE_API_KEY` in `.env` and restart Streamlit.
- **Authentication or model error:** Check the key, Google AI account access, and `GEMINI_MODEL`. The UI reports a safe error; operational context is written to the application log.
- **Cannot save history:** Check that the configured database directory is writable. The default `data` directory is created automatically when needed.
- **PowerShell blocks activation:** Use `py -m pip install -r requirements.txt` and `py -m streamlit run app/main.py` from the environment, or follow your organization's approved execution policy.

## Workshop

The companion [WORKSHOP.md](WORKSHOP.md) contains the trainer agenda, participant exercises, prompt sequence, acceptance criteria, and improvement notes for the original handbook.

## License

This project is provided under the MIT License; see [LICENSE](LICENSE).
