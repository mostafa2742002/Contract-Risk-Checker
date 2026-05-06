from pydantic import BaseModel, Field


class Risk(BaseModel):
    type: str
    explanation: str
    suggested_fix: str
    confidence: float = Field(ge=0.0, le=1.0)
    evidence: str