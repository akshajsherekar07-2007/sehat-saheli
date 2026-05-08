"""
Health camp model for government health camp alerts.
"""

from datetime import date

from sqlalchemy import Boolean, Date, Float, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import BaseModel


class HealthCamp(BaseModel):
    """A government or NGO health camp event."""

    __tablename__ = "health_camps"

    name: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    location: Mapped[str] = mapped_column(String(300), nullable=False)
    district: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    state: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    latitude: Mapped[float | None] = mapped_column(Float, nullable=True)
    longitude: Mapped[float | None] = mapped_column(Float, nullable=True)
    event_date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    contact_phone: Mapped[str | None] = mapped_column(String(15), nullable=True)
    organizer: Mapped[str | None] = mapped_column(String(200), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    def __repr__(self) -> str:
        return f"<HealthCamp(name={self.name}, date={self.event_date})>"
