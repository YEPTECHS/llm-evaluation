from pydantic import BaseModel, Field
from typing import Dict, List

from .metric import MetricDefinition


class EvaluationResult(BaseModel):
    ConversationID: str
    ConversationContent: str
    scores: Dict[str, float]
    reasons: Dict[str, str]


class EvaluationRequest(BaseModel):
    metrics: List[MetricDefinition] = Field(
        default_factory=list,
        description="List of metrics to evaluate the conversation with.",
    )
