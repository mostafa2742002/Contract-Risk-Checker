from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


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