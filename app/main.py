from fastapi import FastAPI

from schemas.user_contract_request import UserCreateRequest

app = FastAPI()


@app.post("/api/contract/analysis")
def contract_analysis(request: UserCreateRequest):
    return {
        "message": "your contract has been analyzed successfully",
        "content": request.content
    }