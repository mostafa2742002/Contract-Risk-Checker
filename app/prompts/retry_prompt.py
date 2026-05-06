def retry_prompt(error_message: str) -> str:
    return (
        "\n\nIMPORTANT RETRY INSTRUCTION:\n"
        "Your previous response was invalid.\n"
        f"Reason: {error_message}\n"
        "Return ONLY valid JSON that matches the required schema."
    )