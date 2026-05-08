"""
Cycle tracking (health dashboard) Pydantic schemas.
"""

from datetime import date, datetime
from pydantic import BaseModel, Field


class CycleLogCreate(BaseModel):
    period_start: date
    period_end: date | None = None
    cycle_length: int | None = Field(None, ge=15, le=60)
    symptoms: dict | None = None
    notes: str | None = None


class CycleLogOut(BaseModel):
    id: str
    period_start: date
    period_end: date | None = None
    cycle_length: int | None = None
    symptoms: dict | None = None
    notes: str | None = None
    created_at: datetime

    model_config = {"from_attributes": True}


class CyclePrediction(BaseModel):
    predicted_start: date
    average_cycle_length: int
    based_on_entries: int


class CycleAnalytics(BaseModel):
    total_logs: int = 0
    average_cycle_length: float = 0.0
    average_period_length: float = 0.0
    shortest_cycle: int | None = None
    longest_cycle: int | None = None
