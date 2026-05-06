from pydantic import BaseModel

from app.schemas.risk import Risk

class AIAnalysisResponse(BaseModel):
    risks: list[Risk]
