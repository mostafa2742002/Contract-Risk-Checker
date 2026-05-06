import json
import os
import sys

from pathlib import Path
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError


PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(env_path)

from app.exceptions.glopal_exception_handler import (
    json_decode_exception_handler,
    validation_error_handler,
    validation_exception_handler,
)
from app.schemas.user_contract_request import UserCreateRequest
from app.services.contract_analysis_service import analyze_contract


app = FastAPI()


def register_exception_handlers() -> None:
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(json.JSONDecodeError, json_decode_exception_handler)
    app.add_exception_handler(ValidationError, validation_error_handler)

register_exception_handlers()



@app.post("/api/contract/analysis")
async def contract_analysis_api(request: UserCreateRequest):
    return await analyze_contract(request.contract)
