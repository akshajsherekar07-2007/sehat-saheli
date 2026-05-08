"""
User repository — extends BaseRepository with user-specific queries.
"""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):
    """Data access layer for User entities."""

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(User, session)

    async def get_by_phone(self, phone: str) -> User | None:
        """Find a user by phone number (used for login)."""
        stmt = select(User).where(User.phone == phone)
        result = await self._session.execute(stmt)
        return result.scalars().first()

    async def phone_exists(self, phone: str) -> bool:
        """Check if a phone number is already registered."""
        user = await self.get_by_phone(phone)
        return user is not None
