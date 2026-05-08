"""
Authentication API router.
Handles registration, login, token refresh, and profile management.
"""

from fastapi import APIRouter, status

from app.core.dependencies import CurrentUserId, DBSession
from app.schemas.auth import (
    RefreshTokenRequest,
    TokenResponse,
    UserLoginRequest,
    UserProfileResponse,
    UserRegisterRequest,
    UserUpdateRequest,
)
from app.schemas.common import MessageResponse
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post(
    "/register",
    response_model=TokenResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
)
async def register(data: UserRegisterRequest, db: DBSession) -> TokenResponse:
    """Create a new user account and return JWT tokens."""
    service = AuthService(db)
    return await service.register(data)


@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Login with phone and password",
)
async def login(data: UserLoginRequest, db: DBSession) -> TokenResponse:
    """Authenticate and return JWT tokens."""
    service = AuthService(db)
    return await service.login(data.phone, data.password)


@router.post(
    "/refresh",
    response_model=TokenResponse,
    summary="Refresh access token",
)
async def refresh_token(data: RefreshTokenRequest, db: DBSession) -> TokenResponse:
    """Issue new tokens using a valid refresh token."""
    service = AuthService(db)
    return await service.refresh_token(data.refresh_token)


@router.get(
    "/me",
    response_model=UserProfileResponse,
    summary="Get current user profile",
)
async def get_profile(user_id: CurrentUserId, db: DBSession) -> UserProfileResponse:
    """Fetch the authenticated user's profile."""
    service = AuthService(db)
    return await service.get_profile(user_id)


@router.put(
    "/me",
    response_model=UserProfileResponse,
    summary="Update current user profile",
)
async def update_profile(
    data: UserUpdateRequest,
    user_id: CurrentUserId,
    db: DBSession,
) -> UserProfileResponse:
    """Update the authenticated user's profile."""
    service = AuthService(db)
    return await service.update_profile(user_id, data)
