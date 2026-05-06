
OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "llama3.1:8b"
REQUEST_TIMEOUT_SECONDS = 60.0
import httpx

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

