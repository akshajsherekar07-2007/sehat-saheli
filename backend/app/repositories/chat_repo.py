"""
Chat repository — extends BaseRepository with chat-specific queries.
"""

from typing import Sequence

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.chat import ChatMessage, ChatSession
from app.repositories.base import BaseRepository


class ChatSessionRepository(BaseRepository[ChatSession]):
    """Data access layer for ChatSession entities."""

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(ChatSession, session)

    async def get_user_sessions(
        self,
        user_id: str,
        *,
        skip: int = 0,
        limit: int = 20,
    ) -> Sequence[ChatSession]:
        """Get all chat sessions for a user, most recent first."""
        stmt = (
            select(ChatSession)
            .where(ChatSession.user_id == user_id)
            .order_by(ChatSession.updated_at.desc())
            .offset(skip)
            .limit(limit)
        )
        result = await self._session.execute(stmt)
        return result.scalars().all()

    async def get_user_session(self, session_id: str, user_id: str) -> ChatSession | None:
        """Get a specific session ensuring it belongs to the user."""
        stmt = select(ChatSession).where(
            ChatSession.id == session_id,
            ChatSession.user_id == user_id,
        )
        result = await self._session.execute(stmt)
        return result.scalars().first()

    async def count_user_sessions(self, user_id: str) -> int:
        """Count sessions belonging to a user."""
        stmt = select(func.count()).select_from(ChatSession).where(ChatSession.user_id == user_id)
        result = await self._session.execute(stmt)
        return result.scalar_one()


class ChatMessageRepository(BaseRepository[ChatMessage]):
    """Data access layer for ChatMessage entities."""

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(ChatMessage, session)

    async def get_session_messages(
        self,
        session_id: str,
        *,
        skip: int = 0,
        limit: int = 50,
    ) -> Sequence[ChatMessage]:
        """Get all messages in a session, chronologically ordered."""
        stmt = (
            select(ChatMessage)
            .where(ChatMessage.session_id == session_id)
            .order_by(ChatMessage.created_at.asc())
            .offset(skip)
            .limit(limit)
        )
        result = await self._session.execute(stmt)
        return result.scalars().all()

    async def get_recent_context(
        self,
        session_id: str,
        *,
        limit: int = 10,
    ) -> Sequence[ChatMessage]:
        """Get the most recent messages for AI context window."""
        stmt = (
            select(ChatMessage)
            .where(ChatMessage.session_id == session_id)
            .order_by(ChatMessage.created_at.desc())
            .limit(limit)
        )
        result = await self._session.execute(stmt)
        messages = result.scalars().all()
        return list(reversed(messages))  # Return in chronological order

    async def count_session_messages(self, session_id: str) -> int:
        """Count messages in a session."""
        stmt = (
            select(func.count())
            .select_from(ChatMessage)
            .where(ChatMessage.session_id == session_id)
        )
        result = await self._session.execute(stmt)
        return result.scalar_one()
