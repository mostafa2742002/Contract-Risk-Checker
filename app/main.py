from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from exceptions.glopal_exception_handler import validation_exception_handler
from schemas.user_contract_request import UserCreateRequest

app = FastAPI()


app.add_exception_handler(
    RequestValidationError,
    validation_exception_handler
)




@app.post("/api/contract/analysis")
def contract_analysis(request: UserCreateRequest):
    return {
        "message": "your contract has been analyzed successfully",
        "content": request.content
    }