import httpx
from services.ai.ollama import call_ollama
from services.ai.gemini import call_gemini


async def get_ai_response(prompt: str) -> str:

    try:
        response = await call_ollama(prompt)
        return response
    except (httpx.ConnectError, httpx.TimeoutException, httpx.RequestError) as ollama_error:
        print(f"Ollama failed: {ollama_error}. Falling back to Gemini...")
    except Exception as e:
        print(f"Ollama unexpected error: {e}. Falling back to Gemini...")
    
    try:
        response = await call_gemini(prompt)
        return response
    except Exception as gemini_error:
        raise RuntimeError(
            f"Both AI providers failed. Gemini error: {gemini_error}"
        )
