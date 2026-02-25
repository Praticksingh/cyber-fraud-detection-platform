from pydantic import BaseModel
from typing import Optional, List


class FraudRequest(BaseModel):
    """Request model for fraud analysis."""
    phone_number: Optional[str] = None
    message_content: Optional[str] = None


class FraudResponse(BaseModel):
    """Response model for fraud analysis results."""
    risk_score: int
    explanation: str
    risk_level: str
    confidence: int
    primary_reason: str
    contributing_factors: List[str]
    recommendation: str
    threat_category: str
