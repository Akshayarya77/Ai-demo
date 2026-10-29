# Trainer Handbook: AI Resume Analyzer Workshop

**Project:** AI Resume Analyzer & Job Recommendation System  
**Duration:** 3–4 hours  
**Audience:** Beginners, faculty members, and students  
**Suggested tools:** VS Code, an AI coding assistant, Git, Python, Streamlit, LangChain, Google Gemini API

## Workshop purpose

Participants use an AI coding assistant to move from product needs to a tested, documented prototype. The assistant generates code, but participants remain responsible for reviewing requirements, validating outputs, and deciding whether changes are safe.

### Learning outcomes

By the end, participants should be able to:

- Turn a problem statement into testable requirements and acceptance criteria.
- Ask an AI assistant to propose architecture and generate a modular application.
- Review generated code for correctness, privacy, security, and maintainability.
- Create and run deterministic tests with external services mocked.
- Diagnose an error from a traceback and add a regression test.
- Document setup, configuration, limitations, and release steps.

## Run of show

| Time | Module | Participant outcome |
|---|---|---|
| 0:00–0:15 | Product discovery | Agree on users, problem, and non-goals |
| 0:15–0:35 | Requirements | PRD outline and acceptance criteria |
| 0:35–0:55 | Architecture | Data flow, components, and risk decisions |
| 0:55–1:10 | Project structure | Review package boundaries and dependencies |
| 1:10–1:55 | Application generation | Build and run the first working prototype |
| 1:55–2:10 | Break | — |
| 2:10–2:30 | Code review and refactor | Identify and fix prioritized issues |
| 2:30–2:55 | Testing | Mock the API and verify validation/error cases |
| 2:55–3:10 | Debugging | Reproduce and fix a controlled failure |
| 3:10–3:25 | Security and privacy | Complete a threat and data-handling review |
| 3:25–3:40 | Documentation and Git | Update setup docs and prepare a branch/PR |
| 3:40–4:00 | Readiness review | Decide what is demo-ready versus production-blocking |

For a three-hour session, shorten the architecture and documentation discussions, and assign the final readiness review as follow-up work. Do not skip testing or the privacy review.

## Product brief

The placement cell wants to help students understand how clearly a resume communicates their experience and what skills they may want to develop. The prototype accepts pasted resume text and returns:

1. A concise resume summary
2. Technical and soft skills
3. An evidence-based experience assessment
4. Suggested job roles
5. Potential skill gaps
6. Learning suggestions
7. Actionable resume improvements

**Users:** students, job seekers, career counselors, and placement officers.  
**Non-goal:** automatically ranking candidates or making hiring decisions.

## Activity 1 — Product discovery and requirements

Ask the coding assistant:

> Act as a product manager for career services. Draft a concise PRD for a resume-analysis prototype for students and job seekers. Include user needs, business objectives, functional and non-functional requirements, user stories, acceptance criteria, risks, and explicit non-goals. The product must not rank candidates or make hiring decisions. Flag assumptions rather than inventing facts.

Have participants check whether each requirement is testable. Agree on criteria such as:

- Empty and overly long input is rejected before an API call.
- Successful analysis includes every required output section.
- API failures are shown as understandable errors without exposing credentials or resume text.
- Tests run without network access or a real API key.
- Resume text is not written to local storage.
- Saving an analysis, if implemented, requires explicit user action and explains what is stored.

**Discussion:** Why do requirements precede implementation? Which requirements need a measurable acceptance test?

## Activity 2 — Architecture

Prompt:

> Act as a software architect. Propose a simple, testable Python and Streamlit architecture for the approved requirements. Show UI, configuration, analysis service, prompt, persistence (only if explicitly opted in), and test boundaries. Include a text data-flow diagram, error handling, logging, privacy controls, and testing strategy. Do not store raw resumes. Identify which data leaves the user's machine.

Ask the assistant to explain the request flow in plain language and identify failure points. Decide the storage and retention behavior before code generation rather than assuming a database should contain resume data.

**Discussion:** Separation of concerns, API boundaries, least data retention, and what “production-ready” would require beyond a classroom demo.

## Activity 3 — Project structure

Prompt:

> Suggest a minimal folder structure for this prototype that separates Streamlit UI, settings, prompt text, analysis logic, optional report persistence, and tests. For every file, state its responsibility and dependencies. Keep the structure small enough for a beginner to navigate.

Review whether each module has one clear responsibility. Avoid creating empty layers or abstractions without a concrete use.

## Activity 4 — Application generation

Prompt:

> Implement the approved requirements in this repository using Python, Streamlit, LangChain with Google Gemini, and pytest. Keep model calls behind a service boundary, validate input and structured model output, load secrets from environment configuration, and provide actionable UI errors. Add opt-in local report history only if the user knowingly chooses it; never persist the raw resume. Add type hints and focused tests. Show the files changed and the commands needed to run the app and tests.

Build and run the smallest useful vertical slice first: input → validation → mocked analysis → rendered result. Add the real API integration only after the mock path passes.

**Demo input:** a fictional early-career developer resume with skills such as Python, REST APIs, Git, Docker, and SQL. Do not use real student resumes in a public workshop without informed consent.

## Activity 5 — Code review

Prompt:

> Review the changed code against the approved requirements. Report only actionable findings, each with file/line, severity, impact, evidence, and a minimal remediation. Check correctness, input/output validation, privacy, error handling, tests, and maintainability. Do not rewrite code until findings are agreed.

Participants verify each claimed finding in the source and rank it by risk. The assistant's review is a starting point, not proof.

## Activity 6 — Refactoring

Prompt:

> Apply the agreed findings only. Preserve required behavior and existing interfaces. Add or update a regression test for each behavior change, then run the focused test suite and report the exact results.

Review the diff after refactoring. Reject broad rewrites that make the implementation harder to understand or test.

## Activity 7 — Testing

Prompt:

> Write pytest tests for configuration, input validation, successful structured output, malformed model output, Gemini API errors, and optional local persistence. Mock the LangChain Gemini boundary. Tests must be deterministic, require no API key, and make no network requests. Include a command to run the focused tests.

Ask participants to run the tests and inspect assertions. A passing suite is useful evidence, but it does not prove the system is unbiased or production-safe.

## Activity 8 — Debugging

Introduce a controlled defect in a disposable branch or test fixture, for example attempting to index a missing field in a response. Never add the intentional bug to the shared main branch.

Prompt:

> Analyze this traceback and the relevant code. Explain the root cause, the smallest safe fix, and how to prevent recurrence. First propose a regression test that fails before the fix. Do not infer values that are not present in the traceback or source.

Run the regression test before and after the fix; show that it catches the defect and then passes.

## Activity 9 — Security and privacy review

Prompt:

> Review this application for secret handling, input validation, data sent to external services, persistence and retention, logging, error messages, dependency risks, and misuse as a hiring tool. Separate confirmed issues from recommendations, assign severity, cite evidence, and give minimal remediation steps. Do not claim a control exists unless you can point to it in the code.

Discuss API-key exposure, sensitive resume data, prompt injection through pasted text, overly broad logging, third-party processing, access controls, and the risks of biased or fabricated recommendations.

## Activity 10 — Documentation

Prompt:

> Update the README for a beginner. Cover purpose and non-goals, features, architecture, supported Python version, Windows/Linux/macOS setup, environment variables, run and test commands, privacy behavior, troubleshooting, limitations, and future work. Verify commands and filenames against the repository; do not invent options.

Participants execute the setup and test commands rather than trusting generated instructions.

## Activity 11 — Git and GitHub

Prompt:

> Give the non-destructive Git commands for creating a feature branch, reviewing the diff, committing related changes, pushing the branch, and opening a pull request. Include a short conventional commit example and a PR checklist for tests, secrets, privacy, and documentation. Do not run commands that overwrite or discard uncommitted work.

Suggested sequence:

```text
git status
git switch -c feature/resume-analysis
git diff
git add <reviewed-files>
git commit -m "feat: add resume analysis prototype"
git push -u origin feature/resume-analysis
```

Use pull requests for review. Protect the default branch and avoid committing `.env`, real resumes, or local report databases.

## Activity 12 — Readiness review

Prompt:

> Review this prototype as a product manager, architect, developer, QA lead, security reviewer, and operations lead. Score requirements coverage, correctness, privacy, testability, accessibility, documentation, and deployment readiness separately. Cite evidence, list blockers, and distinguish demo readiness from production readiness. Do not give a single score that hides unresolved safety risks.

The expected outcome is a decision and prioritized follow-up list—not an unsupported “production-ready” label.

## Review notes and recommended improvements to the source handbook

The original workshop outline is a useful lifecycle map, but several changes make it safer and more teachable:

1. **Scope:** Twelve full lifecycle stages exceed a realistic three-hour beginner session. Keep core requirements, implementation, tests, and privacy review in the live session; make Git/release and readiness work optional or follow-up.
2. **Acceptance criteria:** Define measurable behaviors before generating code, especially input bounds, required output fields, safe failure behavior, and data persistence.
3. **Privacy:** State clearly what resume data is sent to the model provider, whether it is retained, who can access it, and how students give consent. Use fictional resumes for demos.
4. **Employment fairness:** Explicitly prohibit candidate ranking and hiring decisions. Require human review and explain that model output can be inaccurate or biased.
5. **Security detail:** Add prompt-injection handling, output/schema validation, rate and cost limits, dependency updates, database access/retention, and secret-rotation guidance to the review checklist.
6. **Test-first debugging:** Introduce bugs only in disposable branches and require a regression test before the fix. Mock external APIs for all automated tests.
7. **Evidence-based AI use:** Ask assistants to cite files/lines and separate observed facts from assumptions. Participants should inspect generated diffs and run commands themselves.
8. **Release advice:** Replace “merge branch” and “push to GitHub” as unconditional steps with reviewed pull requests, secret scanning, branch protection, and a release checklist.
9. **Production claims:** Treat a classroom demo as a prototype. A real deployment needs a privacy/legal review, accessibility testing, monitoring, retention policy, model evaluation, and incident handling.

## Facilitator checklist

- Prepare a Python environment and verify Streamlit starts before the session.
- Use synthetic resumes and a workshop API key with appropriate limits.
- Keep `.env` out of screen shares, commits, and generated logs.
- Have participants inspect each diff, run tests, and explain one design decision.
- End by asking what evidence would be required before processing real resumes.
