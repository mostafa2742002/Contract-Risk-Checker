import json

import httpx
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError

from exceptions.glopal_exception_handler import json_decode_exception_handler, validation_error_handler, validation_exception_handler
from prompts.dynamic_prompt import generate_dynamic_prompt
from prompts.retry_prompt import retry_prompt
from schemas.ai_analysis_response import AIAnalysisResponse
from schemas.user_contract_request import UserCreateRequest


app = FastAPI()
OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "llama3.1:8b"
REQUEST_TIMEOUT_SECONDS = 60.0
MAX_RETRIES = 2


def register_exception_handlers() -> None:
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(json.JSONDecodeError, json_decode_exception_handler)
    app.add_exception_handler(ValidationError, validation_error_handler)


async def call_ollama(prompt: str) -> str:
    ollama_request = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False,
    }

    async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT_SECONDS) as client:
        response = await client.post(OLLAMA_URL, json=ollama_request)

    response.raise_for_status()
    ollama_response = response.json()
    return ollama_response.get("response", "")


def parse_and_validate_ai_response(ai_text_response: str) -> AIAnalysisResponse:
    ai_json_response = json.loads(ai_text_response)
    return AIAnalysisResponse.model_validate(ai_json_response)


register_exception_handlers()







@app.post("/api/contract/analysis")
async def contract_analysis(request: UserCreateRequest):
    base_prompt = generate_dynamic_prompt(request.contract)
    prompt = base_prompt
    last_error = None

    for _ in range(MAX_RETRIES + 1):
        ai_text_response = await call_ollama(prompt)

        try:
            validated_response = parse_and_validate_ai_response(ai_text_response)

            return {
                "message": "Your contract has been analyzed successfully.",
                "content": validated_response,
            }
        except json.JSONDecodeError as exc:
            last_error = exc
            prompt = base_prompt + retry_prompt("Invalid JSON format")
        except ValidationError as exc:
            last_error = exc
            prompt = base_prompt + retry_prompt("JSON does not match required schema")

    if last_error is None:
        raise RuntimeError("Unexpected retry flow without a captured error")

    raise last_error


