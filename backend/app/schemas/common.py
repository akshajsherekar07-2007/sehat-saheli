"""
Common/shared Pydantic schemas used across multiple features.
"""

from typing import Generic, TypeVar

from pydantic import BaseModel, ConfigDict

T = TypeVar("T")


class HealthResponse(BaseModel):
    """API health check response."""
    status: str = "healthy"
    app: str
    version: str = "1.0.0"


class MessageResponse(BaseModel):
    """Generic message response for simple operations."""
    message: str


class ErrorResponse(BaseModel):
    """Structured error response returned by exception handlers."""
    error_code: str
    message: str
    details: dict | list | str | None = None


class PaginationMeta(BaseModel):
    """Pagination metadata for list endpoints."""
    page: int
    per_page: int
    total: int
    total_pages: int


class PaginatedResponse(BaseModel, Generic[T]):
    """Generic paginated response wrapper — reusable for any list endpoint."""
    model_config = ConfigDict(arbitrary_types_allowed=True)

    data: list[T]
    pagination: PaginationMeta
