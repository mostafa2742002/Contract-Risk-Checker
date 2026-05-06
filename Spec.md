# Contract Risk Checker Specification

## 1. Project Overview
**Project Name:** Contract Risk Checker

**Goal:**  
Build a system that analyzes employment contracts and detects common legal or business risks using AI.


### Risk Definition

A risk is a contract clause that may negatively affect the employee or create legal/business concerns.

The system currently detects risks related to:
- Termination
- Probation
- Exclusivity

The AI should identify risky wording, not only the existence of a clause.

## 2. Scope

### In Scope
- Users can submit plain-text employment contracts for analysis.
- The system analyzes contracts for three risk categories:
1. Termination
2. Probation
3. Exclusivity



### Out of Scope
- The system does not support PDF, image, or scanned-document inputs.
- The system only detects risks related to the supported categories.

### Assumptions

- Contracts are written in English.
- Users submit readable plain text contracts.
- Input text size is within the AI model context limit.
- AI services are available during request processing.
- The system is designed for employment contracts only.

## 3. Functional Requirements

### Input
- The system must accept plain-text contract input.

### Output Schema
- The system must return JSON with a defined schema
- Each risk object must include:
type , explanation, suggested_fix, confidence, evidence
- The system should return one of these risks (Termination, Probation, Exclusivity)
### Example Output

```json
{
  "risks": [
    {
      "type": "Termination",
      "explanation": "The clause allows termination without prior notice.",
      "suggested_fix": "Require a minimum notice period before termination.",
      "confidence": 0.92,
      "evidence": "The employer may terminate the employee’s contract at any time without prior notice or compensation."
    }
  ]
}
```

- confidence must be a float value between 0 and 1.

### Error Response

The system should return structured error responses.

Example:

```json
{
  "error": {
    "code": "INVALID_INPUT",
    "message": "Only plain text contracts are supported."
  }
}
```

Possible error codes:
- INVALID_INPUT
- AI_RESPONSE_INVALID
- AI_SERVICE_UNAVAILABLE

## 4. High-Level Flow

1. User submits contract text.
2. Backend validates the input format.
3. Contract text is sent to the AI model.
4. AI returns structured JSON risks.
5. Backend validates the AI response schema.
6. If validation fails, retry logic is triggered.
7. Valid results are returned to the user.


## 5. Non-Functional Requirements

### Privacy
- Contract data should only be used for risk analysis.
- The system should avoid storing contract text.
- Sensitive contract information should not appear in logs or error messages.

### Reliability
- The system must validate that the AI response matches the expected JSON schema.
- If the AI returns malformed or invalid JSON, the backend should retry the request.
- Retry attempts should be limited to a maximum of 2 retries.
- If the primary AI model is unavailable, the system should use a fallback AI provider when possible.

## 6. Limitations

- AI-generated results may contain false positives or false negatives.
- Only English plain-text contracts are currently supported.
- The system only checks risks related to Termination, Probation, and Exclusivity.

## 7. Acceptance Criteria

- AC1 Given an input text containing a risky probation clause, the system returns at least one risk with type="Probation" and includes evidence from the contract.

- AC2 Given an input text containing a risky termination clause, the system returns at least one risk with type="Termination" and includes evidence from the contract.

- AC3 Given an input text containing a strict exclusivity clause, the system returns at least one risk with type="Exclusivity" and includes evidence from the contract.

- AC4 The system returns valid JSON that conforms to the defined response schema.

- AC5 Given an input text containing multiple supported risks, the system returns all detected risks in the response.

- AC6 Given an unsupported input type (such as PDF), the system returns a structured error response.

- AC7 If the AI returns malformed or invalid JSON, the backend validator detects the issue.

- AC8 If AI response validation fails, the system retries the request up to 2 times.

- AC9 If the primary AI provider is unavailable, the system attempts to use a fallback AI provider.

## 8. Test Cases

### TC1 — Termination Without Notice

**Input text:**

```text
The employer may terminate the employee’s contract at any time without prior notice or compensation.
```
**Expected risk types:**
- Termination

**Special expectations:**

- The result must include an evidence quote from the input.
- The evidence should reference “without prior notice”.
- Confidence must be between 0 and 1.


### TC2 — Long Probation Period

**Input text:**

```text
The employee will be subject to a probation period of twelve months, during which the employer may end the employment relationship immediately.
```

**Expected risk types:**
- Probation
- Termination

**Special expectations:**

- The result should include at least one Probation risk.
- The result may also include a Termination risk because of immediate ending.
- Each returned risk must include explanation, suggested_fix, confidence, and evidence.



### TC3 — Strict Exclusivity Clause

**Input text:**

```text
The employee must not work for any other company, client, or business during the entire employment period, even outside working hours.
```

**Expected risk types:**
- Exclusivity

**Special expectations:**

- The evidence field should quote the exclusivity restriction.
- The suggested_fix should recommend allowing outside work where there is no conflict of interest.



### TC4 — Multiple Risks in One Contract Snippet

**Input text:**

```text
The first nine months of employment are considered a probation period. During this period, the company may terminate the employee immediately without notice. The employee is also prohibited from working for any other business.
```

**Expected risk types:**
- Exclusivity
- Probation
- Termination

**Special expectations:**

- The system should return multiple risks.
- Each risk must have its own evidence quote.
- The output must remain valid JSON.


### TC5 — Safe Contract Text With No Clear Risk

**Input text:**

```text
The employee is entitled to paid annual leave according to applicable employment law. Either party may terminate the contract by giving thirty days written notice.
```

**Expected risk types:**
- None

**Special expectations:**

- The system should return an empty risks array.
- The output must still match the JSON schema.
- The output must remain valid JSON.
