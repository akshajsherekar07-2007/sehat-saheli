"""
Chat API router.
Handles chat sessions and message flow with AI chatbot.
"""

from fastapi import APIRouter, Query, status

from app.core.dependencies import CurrentUserId, DBSession
from app.schemas.chat import (
    ChatMessageRequest,
    ChatMessageResponse,
    ChatSendResponse,
    ChatSessionCreateRequest,
    ChatSessionResponse,
)
from app.schemas.common import MessageResponse
from app.services.chat_service import ChatService

router = APIRouter(prefix="/chat", tags=["Chat"])


@router.post(
    "/sessions",
    response_model=ChatSessionResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new chat session",
)
async def create_session(
    data: ChatSessionCreateRequest,
    user_id: CurrentUserId,
    db: DBSession,
) -> ChatSessionResponse:
    """Start a new AI chat conversation."""
    service = ChatService(db)
    return await service.create_session(user_id, data)


@router.get(
    "/sessions",
    response_model=list[ChatSessionResponse],
    summary="List user's chat sessions",
)
async def list_sessions(
    user_id: CurrentUserId,
    db: DBSession,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
) -> list[ChatSessionResponse]:
    """Get all chat sessions for the authenticated user."""
    service = ChatService(db)
    return await service.get_user_sessions(user_id, skip=skip, limit=limit)


@router.post(
    "/sessions/{session_id}/messages",
    response_model=ChatSendResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Send a message and get AI response",
)
async def send_message(
    session_id: str,
    data: ChatMessageRequest,
    user_id: CurrentUserId,
    db: DBSession,
) -> ChatSendResponse:
    """Send a message in a chat session and receive an AI response."""
    service = ChatService(db)
    return await service.send_message(session_id, user_id, data)


@router.get(
    "/sessions/{session_id}/messages",
    response_model=list[ChatMessageResponse],
    summary="Get session messages",
)
async def get_messages(
    session_id: str,
    user_id: CurrentUserId,
    db: DBSession,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
) -> list[ChatMessageResponse]:
    """Get paginated messages for a chat session."""
    service = ChatService(db)
    return await service.get_session_messages(session_id, user_id, skip=skip, limit=limit)


@router.delete(
    "/sessions/{session_id}",
    response_model=MessageResponse,
    summary="Delete a chat session",
)
async def delete_session(
    session_id: str,
    user_id: CurrentUserId,
    db: DBSession,
) -> MessageResponse:
    """Delete a chat session and all its messages."""
    service = ChatService(db)
    await service.delete_session(session_id, user_id)
    return MessageResponse(message="Chat session deleted successfully")
