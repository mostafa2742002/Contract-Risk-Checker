import json
from pydantic import ValidationError

from prompts.dynamic_prompt import generate_dynamic_prompt
from prompts.retry_prompt import retry_prompt
from schemas.ai_analysis_response import AIAnalysisResponse
from services.ai.ai_provider import get_ai_response

MAX_RETRIES = 2


def parse_and_validate_ai_response(ai_text_response: str) -> AIAnalysisResponse:
    ai_json_response = json.loads(ai_text_response)
    return AIAnalysisResponse.model_validate(ai_json_response)



async def analyze_contract(contract_content: str) -> AIAnalysisResponse:
    base_prompt = generate_dynamic_prompt(contract_content)
    prompt = base_prompt
    last_error = None

    for _ in range(MAX_RETRIES + 1):
        ai_text_response = await get_ai_response(prompt)

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