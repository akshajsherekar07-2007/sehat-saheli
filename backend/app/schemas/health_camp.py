"""
Health camp Pydantic schemas.
"""

from datetime import date
from pydantic import BaseModel


class HealthCampOut(BaseModel):
    """Health camp response schema."""
    id: str
    name: str
    description: str | None = None
    location: str
    district: str
    state: str
    latitude: float | None = None
    longitude: float | None = None
    event_date: date
    contact_phone: str | None = None
    organizer: str | None = None
    is_active: bool

    model_config = {"from_attributes": True}
