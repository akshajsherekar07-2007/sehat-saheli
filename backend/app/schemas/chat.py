"""
Chat-related Pydantic schemas for request/response validation.
"""

from datetime import datetime

from pydantic import BaseModel, Field


class ChatSessionCreateRequest(BaseModel):
    """Create a new chat session."""
    title: str = Field("New Chat", max_length=200)
    language: str = Field("en", description="Chat language code")


class ChatSessionResponse(BaseModel):
    """Chat session summary response."""
    id: str
    title: str
    language: str
    created_at: datetime
    updated_at: datetime
    message_count: int = 0

    class Config:
        from_attributes = True


class ChatMessageRequest(BaseModel):
    """Send a message in a chat session."""
    content: str = Field(..., min_length=1, max_length=2000, description="User message")
    language: str = Field("en", description="Message language code")


class ChatMessageResponse(BaseModel):
    """A single chat message."""
    id: str
    role: str
    content: str
    language: str
    created_at: datetime

    class Config:
        from_attributes = True


class ChatSendResponse(BaseModel):
    """Response after sending a message — includes both user msg and AI reply."""
    user_message: ChatMessageResponse
    assistant_message: ChatMessageResponse
    disclaimer: str | None = None
