"""
Base model mixin providing common fields and utilities for all ORM models.
Every model inherits from this to get UUID PK, timestamps, and serialization.
"""

import uuid
from datetime import datetime, timezone

from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


def generate_uuid() -> str:
    """Generate a new UUID4 string."""
    return str(uuid.uuid4())


def utc_now() -> datetime:
    """Current UTC timestamp."""
    return datetime.now(timezone.utc)


class TimestampMixin:
    """Mixin that adds created_at and updated_at timestamps to any model."""

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now,
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now,
        onupdate=utc_now,
        nullable=False,
    )


class BaseModel(Base, TimestampMixin):
    """
    Abstract base model with UUID primary key and timestamps.
    All domain models should extend this.
    """

    __abstract__ = True

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=generate_uuid,
        nullable=False,
    )

    def to_dict(self) -> dict:
        """Serialize model to dictionary (excludes relationships)."""
        return {
            column.name: getattr(self, column.name)
            for column in self.__table__.columns
        }
