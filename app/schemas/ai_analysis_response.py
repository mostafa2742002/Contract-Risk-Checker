from pydantic import BaseModel

from schemas.risk import Risk

class AIAnalysisResponse(BaseModel):
    risks: list[Risk]

