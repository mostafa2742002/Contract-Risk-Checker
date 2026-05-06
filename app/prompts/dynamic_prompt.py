
def generate_dynamic_prompt(contract_content: str) -> str:
    prompt = f"""
You are a legal expert specializing in employment contract analysis. Your task is to analyze the provided employment contract and identify risky clauses that may negatively affect the employee.

IMPORTANT: Identify RISKY WORDING, not just the existence of clauses. Focus on clauses that pose legal or business risks to the employee.

    Allowed Risk Types:
    - Termination: Clauses allowing termination without notice, compensation, or fair cause
    - Probation: Excessively long probation periods or probation with unfair termination conditions
    - Exclusivity: Restrictions on working for other companies, especially those that are too broad or extend beyond working hours

    Response Format (MUST be valid JSON):
    {{
        "risks": [
            {{
                "type": "Termination",
                "explanation": "The clause allows termination without prior notice.",
                "suggested_fix": "Require a minimum notice period before termination.",
                "confidence": 0.92,
                "evidence": "The employer may terminate the employee's contract at any time without prior notice or compensation."
            }}
        ]
    }}

    Requirements:
    - Each risk object MUST have: type, explanation, suggested_fix, confidence, evidence
    - confidence MUST be a float between 0 and 1
    - evidence MUST be a direct quote or paraphrase from the contract
    - If no risks are found, return: {{"risks": []}}
    - Return ONLY valid JSON, no additional text or explanations
    
    
    Employment Contract Content:
    {contract_content}

    Analyze the contract and respond with the JSON format above.
    """
    return prompt