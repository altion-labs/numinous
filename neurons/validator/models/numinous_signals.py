from datetime import datetime
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class WeightedSignal(BaseModel):
    headline: str
    source: str
    timestamp: datetime
    relevance_score: float = Field(..., ge=0.0, le=1.0)
    impact_score: float = Field(..., ge=0.0, le=1.0)
    direction: Literal["supports_yes", "supports_no", "neutral"]
    rationale: str
    source_url: str | None = None

    model_config = ConfigDict(extra="allow")


class SourceWeight(BaseModel):
    source_name: str
    event_count: int
    avg_relevance_score: float = Field(..., ge=0.0, le=1.0)
    avg_impact_score: float = Field(..., ge=0.0, le=1.0)

    model_config = ConfigDict(extra="allow")


class ProcessingMetadata(BaseModel):
    duration_seconds: float
    llm_scored_count: int
    total_ingested_events: int
    question_text: str
    market_yes_price: float | None = None

    model_config = ConfigDict(extra="allow")


class SignalsResponse(BaseModel):
    signals: list[WeightedSignal]
    source_weights: list[SourceWeight]
    total_event_count: int
    filtered_count: int
    failed_sources: list[str] = Field(default_factory=list)
    question_context: str
    processing_metadata: ProcessingMetadata

    model_config = ConfigDict(extra="allow")


COST_PER_CALL = Decimal("0.001")


def calculate_cost() -> Decimal:
    return COST_PER_CALL
