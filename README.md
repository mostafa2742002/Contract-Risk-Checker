# Contract Risk Checker

Lightweight service to analyze employment contract text for common risks (Termination, Probation, Exclusivity) using local and cloud AI providers with a fallback strategy.

## Summary
- Accepts plain-text employment contracts and returns a structured JSON list of detected risks.
- Primary AI provider: Ollama (local). Backup provider: Gemini (cloud) — automatic failover.
- Responses are validated against a strict JSON schema.

## Quickstart

Requirements: Python 3.11+ and a virtual environment.

1. Create and activate a virtualenv:

```bash
python -m venv venv
source venv/bin/activate
```

2. Install dependencies:

```bash
pip install fastapi uvicorn httpx pydantic python-dotenv pytest pytest-asyncio
```

3. Copy the example env and set secrets:

```bash
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY
```

4. Run the app (from project root):

```bash
cd app
uvicorn main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.

## API

POST /api/contract/analysis

Request body (JSON):

```json
{ "contract": "<plain text contract here>" }
```

Response (successful):

```json
{
  "message": "Your contract has been analyzed successfully.",
  "content": {
    "risks": [ /* array of risk objects */ ]
  }
}
```

Each risk object contains: `type`, `explanation`, `suggested_fix`, `confidence` (0..1), `evidence`.

## Configuration

All configuration and secrets are centralized in `app/config.py` and read from environment variables. Use `.env` in the project root to set:

- `GEMINI_API_KEY` — Gemini API key
- `OLLAMA_URL` / `OLLAMA_MODEL` — (optional)
- `REQUEST_TIMEOUT_SECONDS`, `MAX_RETRIES`

Do not commit your `.env` to version control (it is included in `.gitignore`).

## Tests

Automated tests are in `app/tests/`. They validate:

- JSON schema validity
- Evidence field presence
- Stable behavior for key test cases (from Spec.md)

Run tests from project root:

```bash
cd app
pytest tests/ -v
```

## Example responses

Below are example AI responses used in tests:

- Single-risk example:

```json
{
  "risks": [
    {
      "type": "Termination",
      "explanation": "No notice period",
      "suggested_fix": "Add 30 day notice requirement",
      "confidence": 0.92,
      "evidence": "employer may terminate at any time without notice"
    }
  ]
}
```

- Multiple-risk example:

```json
{
  "risks": [
    {
      "type": "Probation",
      "explanation": "Long probation",
      "suggested_fix": "Reduce probation",
      "confidence": 0.85,
      "evidence": "probation period of twelve months"
    },
    {
      "type": "Termination",
      "explanation": "Immediate termination",
      "suggested_fix": "Require notice",
      "confidence": 0.88,
      "evidence": "end the employment immediately"
    }
  ]
}
```

## Use of AI Assistance

I used AI tools as a support layer during the assignment, not as a replacement for my own work. I started by brainstorming the task with ChatGPT to clarify requirements and shape the implementation plan. During development, I used Codex and GitHub Copilot to help investigate complex bugs, understand the root cause of errors, and speed up repetitive or boilerplate work such as test writing and README drafting.

I also used AI to review and improve the wording of the Spec.md file after I wrote the first version, so I could make the requirements clearer and easier to follow. In every case, I kept the technical decisions, code changes, and final validation under my own control.

This workflow helped me stay structured and efficient while still producing and reviewing all final outputs myself.