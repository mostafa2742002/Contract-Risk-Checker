import httpx

from app.config import GEMINI_URL, GEMINI_MODEL, GEMINI_API_KEY, REQUEST_TIMEOUT_SECONDS


async def call_gemini(prompt: str) -> str:
    gemini_request = {
        "contents": [
            {
                "parts": [
                    {
                        "text": prompt
                    }
                ]
            }
        ]
    }

    url = f"{GEMINI_URL}?key={GEMINI_API_KEY}"

    async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT_SECONDS) as client:
        response = await client.post(url, json=gemini_request)

    response.raise_for_status() 
    gemini_response = response.json()
    
    candidates = gemini_response.get("candidates", [])
    if candidates:
        content = candidates[0].get("content", {})
        parts = content.get("parts", [])
        if parts:
            return parts[0].get("text", "")
    
    return ""
