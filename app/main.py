from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
import httpx
from exceptions.glopal_exception_handler import validation_exception_handler
from schemas.user_contract_request import UserCreateRequest

app = FastAPI()


app.add_exception_handler(
    RequestValidationError,
    validation_exception_handler
)




@app.post("/api/contract/analysis")
async def contract_analysis(request: UserCreateRequest):
    
    ollama_request = {
        "model": "llama3.1:8b",
        "prompt": request.contract,
        "stream": False 
    }
    
    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(
            "http://localhost:11434/api/generate",
            json=ollama_request
        )
    
    response.raise_for_status()
    ollama_response = response.json()
    
    return {
        "message": "your contract has been analyzed successfully",
        "content": ollama_response.get("response", "")
    }