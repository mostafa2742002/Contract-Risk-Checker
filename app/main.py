from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
import httpx
from prompts.dynamic_prompt import generate_dynamic_prompt
from exceptions.glopal_exception_handler import json_decode_exception_handler, validation_error_handler, validation_exception_handler
from schemas.user_contract_request import UserCreateRequest
import json
from pydantic import ValidationError

from schemas.ai_analysis_response import AIAnalysisResponse


app = FastAPI()


app.add_exception_handler(
    RequestValidationError,
    validation_exception_handler
)
app.add_exception_handler(json.JSONDecodeError, json_decode_exception_handler)
app.add_exception_handler(ValidationError, validation_error_handler)







@app.post("/api/contract/analysis")
async def contract_analysis(request: UserCreateRequest):

    ollama_request = {
        "model": "llama3.1:8b",
        "prompt": generate_dynamic_prompt(request.contract),
        "stream": False
    }

    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(
            "http://localhost:11434/api/generate",
            json=ollama_request
        )

    response.raise_for_status()
    ollama_response = response.json()

    ai_text_response = ollama_response.get("response", "")

    
    ai_json_response = json.loads(ai_text_response)

    validated_response = AIAnalysisResponse.model_validate(
        ai_json_response
    )

    return {
        "message": "Your contract has been analyzed successfully.",
        "content": validated_response
    }