import httpx

from config import OLLAMA_URL, OLLAMA_MODEL, REQUEST_TIMEOUT_SECONDS


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

