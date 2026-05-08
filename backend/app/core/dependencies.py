"""
FastAPI dependencies for dependency injection.
Provides reusable Depends() callables for auth, DB sessions, etc.
"""

from typing import Annotated

import jwt
from fastapi import Depends, Header
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import Settings, get_settings
from app.core.database import get_db_session
from app.core.exceptions import UnauthorizedException
from app.core.security import decode_token

# ── Type aliases for cleaner signatures ──────────────────────────
DBSession = Annotated[AsyncSession, Depends(get_db_session)]
AppSettings = Annotated[Settings, Depends(get_settings)]


async def get_current_user_id(
    authorization: str = Header(..., description="Bearer <token>"),
) -> str:
    """
    Extract and validate the current user ID from the Authorization header.
    Used as a FastAPI dependency for protected routes.
    
    Raises:
        UnauthorizedException: If the token is missing, expired, or invalid.
    """
    if not authorization.startswith("Bearer "):
        raise UnauthorizedException("Invalid authorization header format")

    token = authorization.removeprefix("Bearer ").strip()
    if not token:
        raise UnauthorizedException("Token is required")

    try:
        payload = decode_token(token)
    except jwt.ExpiredSignatureError:
        raise UnauthorizedException("Token has expired")
    except jwt.InvalidTokenError:
        raise UnauthorizedException("Invalid token")

    if payload.get("type") != "access":
        raise UnauthorizedException("Invalid token type")

    user_id = payload.get("sub")
    if not user_id:
        raise UnauthorizedException("Invalid token payload")

    return user_id


# Annotated type for current user dependency
CurrentUserId = Annotated[str, Depends(get_current_user_id)]
