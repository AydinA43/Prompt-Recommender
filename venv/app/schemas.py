from pydantic import BaseModel
from typing import List, Optional

class Recommendation(BaseModel):
    prompt: str
    similarity: float
    reason: str

class RecommendResponse(BaseModel):
    recommendations: List[Recommendation]
    user_id: str