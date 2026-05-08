"""
Learning content models — categories and articles for health education.
"""

from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy import JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel


class LearnCategory(BaseModel):
    """Education content category (e.g., Menstrual Cycle, Nutrition)."""

    __tablename__ = "learn_categories"

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    slug: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    icon: Mapped[str | None] = mapped_column(String(50), nullable=True)
    order_index: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    # ── Relationships ────────────────────────────────────────
    articles = relationship("LearnArticle", back_populates="category", cascade="all, delete-orphan", order_by="LearnArticle.order_index")

    def __repr__(self) -> str:
        return f"<LearnCategory(slug={self.slug})>"


class LearnArticle(BaseModel):
    """A health education article/infographic/video with multilingual content."""

    __tablename__ = "learn_articles"

    category_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("learn_categories.id", ondelete="CASCADE"), nullable=False, index=True
    )
    title: Mapped[dict] = mapped_column(JSON, nullable=False)       # {"en": "...", "hi": "..."}
    content: Mapped[dict] = mapped_column(JSON, nullable=False)     # {"en": "...", "hi": "..."}
    image_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    video_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    content_type: Mapped[str] = mapped_column(String(20), default="article", nullable=False)
    order_index: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    # ── Relationships ────────────────────────────────────────
    category = relationship("LearnCategory", back_populates="articles")

    def __repr__(self) -> str:
        return f"<LearnArticle(id={self.id}, type={self.content_type})>"
