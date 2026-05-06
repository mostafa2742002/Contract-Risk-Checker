from fastapi import FastAPI

app = FastAPI()


@app.get("/api/contract/analysis")
def contract_analysis():
    return {
        "message": "Contract analysis from FastAPI"
    }