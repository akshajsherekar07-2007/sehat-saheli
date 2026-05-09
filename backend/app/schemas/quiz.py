"""
Quiz Pydantic schemas for request/response validation.
"""

from datetime import datetime
from pydantic import BaseModel, Field


# ── Response Schemas ─────────────────────────────────────────────

class QuizCategoryOut(BaseModel):
    id: str
    name: str
    slug: str
    description: str | None = None
    image_url: str | None = None
    quiz_count: int = 0

    model_config = {"from_attributes": True}


class QuizOut(BaseModel):
    id: str
    category_id: str
    question: dict
    options: dict
    correct_option: int = 0
    image_url: str | None = None
    difficulty: str = "medium"

    model_config = {"from_attributes": True}


class QuizWithAnswer(QuizOut):
    """Returned after submitting an attempt — includes correct answer."""
    correct_option: int


class QuizAttemptCreate(BaseModel):
    selected_option: int = Field(..., ge=0, le=3)


class QuizAttemptOut(BaseModel):
    id: str
    quiz_id: str
    selected_option: int
    is_correct: bool
    score: int
    created_at: datetime

    model_config = {"from_attributes": True}


class QuizResultOut(BaseModel):
    attempt: QuizAttemptOut
    correct_option: int
    explanation: str | None = None


class QuizStatsOut(BaseModel):
    total_attempts: int = 0
    correct_count: int = 0
    total_score: int = 0
    accuracy: float = 0.0
