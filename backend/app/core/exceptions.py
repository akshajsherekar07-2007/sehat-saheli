"""
Custom exception classes with structured error responses.
Provides a consistent error format across the entire API.
"""

from typing import Any

from fastapi import HTTPException, status


class AppException(HTTPException):
    """
    Base application exception with structured error details.
    All custom exceptions should extend this class.
    """

    def __init__(
        self,
        status_code: int,
        error_code: str,
        message: str,
        details: Any = None,
    ) -> None:
        self.error_code = error_code
        self.message = message
        self.details = details
        super().__init__(
            status_code=status_code,
            detail={
                "error_code": error_code,
                "message": message,
                "details": details,
            },
        )


class NotFoundException(AppException):
    """Resource not found (404)."""

    def __init__(self, resource: str, identifier: Any = None) -> None:
        detail_msg = f"{resource} not found"
        if identifier:
            detail_msg = f"{resource} with id '{identifier}' not found"
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            error_code="NOT_FOUND",
            message=detail_msg,
        )


class UnauthorizedException(AppException):
    """Authentication failed (401)."""

    def __init__(self, message: str = "Invalid credentials") -> None:
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            error_code="UNAUTHORIZED",
            message=message,
        )


class ForbiddenException(AppException):
    """Insufficient permissions (403)."""

    def __init__(self, message: str = "Insufficient permissions") -> None:
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            error_code="FORBIDDEN",
            message=message,
        )


class ConflictException(AppException):
    """Resource conflict — e.g., duplicate entry (409)."""

    def __init__(self, resource: str, field: str, value: Any) -> None:
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            error_code="CONFLICT",
            message=f"{resource} with {field} '{value}' already exists",
        )


class ValidationException(AppException):
    """Business logic validation failure (422)."""

    def __init__(self, message: str, details: Any = None) -> None:
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            error_code="VALIDATION_ERROR",
            message=message,
            details=details,
        )


class AIServiceException(AppException):
    """AI service failure (503)."""

    def __init__(self, message: str = "AI service temporarily unavailable") -> None:
        super().__init__(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            error_code="AI_SERVICE_ERROR",
            message=message,
        )
