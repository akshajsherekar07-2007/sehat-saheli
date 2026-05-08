"""
Quiz models — categories, questions, and attempt tracking.
"""

from datetime import date

from sqlalchemy import Boolean, Date, ForeignKey, Integer, String, Text
from sqlalchemy import JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel


class QuizCategory(BaseModel):
    """Quiz category grouping (e.g., Menstrual Health, Nutrition)."""

    __tablename__ = "quiz_categories"

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    slug: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    image_url: Mapped[str | None] = mapped_column(String(500), nullable=True)

    # ── Relationships ────────────────────────────────────────
    quizzes = relationship("Quiz", back_populates="category", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<QuizCategory(slug={self.slug})>"


class Quiz(BaseModel):
    """A single quiz question with multilingual support."""

    __tablename__ = "quizzes"

    category_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("quiz_categories.id", ondelete="CASCADE"), nullable=False, index=True
    )
    question: Mapped[dict] = mapped_column(JSON, nullable=False)  # {"en": "...", "hi": "..."}
    options: Mapped[dict] = mapped_column(JSON, nullable=False)    # {"en": [...], "hi": [...]}
    correct_option: Mapped[int] = mapped_column(Integer, nullable=False)
    image_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    difficulty: Mapped[str] = mapped_column(String(20), default="medium", nullable=False)
    is_daily: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    daily_date: Mapped[date | None] = mapped_column(Date, nullable=True)

    # ── Relationships ────────────────────────────────────────
    category = relationship("QuizCategory", back_populates="quizzes")
    attempts = relationship("QuizAttempt", back_populates="quiz", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<Quiz(id={self.id}, difficulty={self.difficulty})>"


class QuizAttempt(BaseModel):
    """Records a user's attempt at answering a quiz question."""

    __tablename__ = "quiz_attempts"

    user_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    quiz_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("quizzes.id", ondelete="CASCADE"), nullable=False, index=True
    )
    selected_option: Mapped[int] = mapped_column(Integer, nullable=False)
    is_correct: Mapped[bool] = mapped_column(Boolean, nullable=False)
    score: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    # ── Relationships ────────────────────────────────────────
    user = relationship("User", back_populates="quiz_attempts")
    quiz = relationship("Quiz", back_populates="attempts")

    def __repr__(self) -> str:
        return f"<QuizAttempt(user={self.user_id}, correct={self.is_correct})>"
