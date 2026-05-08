"""
Authentication service — business logic for registration, login, and token management.
Orchestrates between UserRepository and security utilities.
"""

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.core.exceptions import ConflictException, UnauthorizedException, NotFoundException
from app.core.logging import get_logger
from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    hash_password,
    verify_password,
)
from app.models.user import User
from app.repositories.user_repo import UserRepository
from app.schemas.auth import (
    TokenResponse,
    UserProfileResponse,
    UserRegisterRequest,
    UserUpdateRequest,
)

logger = get_logger(__name__)
settings = get_settings()


class AuthService:
    """Handles user registration, authentication, and profile management."""

    def __init__(self, session: AsyncSession) -> None:
        self._repo = UserRepository(session)

    async def register(self, data: UserRegisterRequest) -> TokenResponse:
        """
        Register a new user account.
        
        Raises:
            ConflictException: If phone number is already registered.
        """
        if await self._repo.phone_exists(data.phone):
            raise ConflictException("User", "phone", data.phone)

        user = User(
            name=data.name,
            phone=data.phone,
            age=data.age,
            address=data.address,
            password_hash=hash_password(data.password),
            preferred_language=data.preferred_language,
        )
        user = await self._repo.create(user)

        logger.info("user_registered", user_id=user.id, phone=user.phone)
        return self._create_token_response(user.id)

    async def login(self, phone: str, password: str) -> TokenResponse:
        """
        Authenticate a user with phone + password.
        
        Raises:
            UnauthorizedException: If credentials are invalid.
        """
        user = await self._repo.get_by_phone(phone)
        if not user or not verify_password(password, user.password_hash):
            raise UnauthorizedException("Invalid phone number or password")

        logger.info("user_logged_in", user_id=user.id)
        return self._create_token_response(user.id)

    async def refresh_token(self, refresh_token: str) -> TokenResponse:
        """
        Issue new tokens using a valid refresh token.
        
        Raises:
            UnauthorizedException: If the refresh token is invalid or expired.
        """
        try:
            payload = decode_token(refresh_token)
        except Exception:
            raise UnauthorizedException("Invalid refresh token")

        if payload.get("type") != "refresh":
            raise UnauthorizedException("Invalid token type")

        user_id = payload.get("sub")
        if not user_id:
            raise UnauthorizedException("Invalid token payload")

        # Verify user still exists
        user = await self._repo.get_by_id(user_id)
        if not user:
            raise UnauthorizedException("User no longer exists")

        logger.info("token_refreshed", user_id=user_id)
        return self._create_token_response(user_id)

    async def get_profile(self, user_id: str) -> UserProfileResponse:
        """
        Fetch the current user's profile.
        
        Raises:
            NotFoundException: If user doesn't exist.
        """
        user = await self._repo.get_by_id(user_id)
        if not user:
            raise NotFoundException("User", user_id)
        return UserProfileResponse.model_validate(user)

    async def update_profile(self, user_id: str, data: UserUpdateRequest) -> UserProfileResponse:
        """
        Update the current user's profile with partial data.
        
        Raises:
            NotFoundException: If user doesn't exist.
        """
        user = await self._repo.get_by_id(user_id)
        if not user:
            raise NotFoundException("User", user_id)

        update_data = data.model_dump(exclude_unset=True)
        if update_data:
            user = await self._repo.update(user, update_data)
            logger.info("profile_updated", user_id=user_id, fields=list(update_data.keys()))

        return UserProfileResponse.model_validate(user)

    @staticmethod
    def _create_token_response(user_id: str) -> TokenResponse:
        """Generate an access + refresh token pair."""
        return TokenResponse(
            access_token=create_access_token(user_id),
            refresh_token=create_refresh_token(user_id),
            expires_in=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        )
