import json

from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import ValidationError


async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError
):
    errors = []

    for error in exc.errors():
        location = error["loc"]
        field = location[-1]

        errors.append({
            "field": field,
            "message": error["msg"]
        })

    return JSONResponse(
        status_code=400,
        content={
            "error": {
                "code": "INVALID_INPUT",
                "message": "Validation failed.",
                "details": errors
            }
        }
    )
    

async def json_decode_exception_handler(
    request: Request,
    exc: json.JSONDecodeError
):
    return JSONResponse(
        status_code=400,
        content={
            "error": {
                "code": "INVALID_JSON",
                "message": "AI response contains invalid JSON."
            }
        }
    )
    


async def validation_error_handler(
    request: Request,
    exc: ValidationError
):
    errors = []

    for error in exc.errors():
        location = error["loc"]
        field = location[-1]

        errors.append({
            "field": field,
            "message": error["msg"]
        })

    return JSONResponse(
        status_code=400,
        content={
                "error": {
                    "code": "AI_RESPONSE_INVALID",
                    "message": "AI response does not match the expected schema."
                }
        }
    )   
    
    
def runtime_exception_handler(
    request: Request,
    exc: RuntimeError
):
    return JSONResponse(
        status_code=500,
        content={
                "error": {
                    "code": "INTERNAL_ERROR",
                    "message": "An unexpected error occurred during contract analysis."
                }
        }
    )
