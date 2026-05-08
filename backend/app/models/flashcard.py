"""
Flashcard models — decks and individual cards with multilingual content.
"""

from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy import JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel


class FlashcardDeck(BaseModel):
    """A themed collection of flashcards (e.g., Anatomy, Puberty)."""

    __tablename__ = "flashcard_decks"

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    slug: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    image_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    category: Mapped[str] = mapped_column(String(50), nullable=False)

    # ── Relationships ────────────────────────────────────────
    cards = relationship("Flashcard", back_populates="deck", cascade="all, delete-orphan", order_by="Flashcard.order_index")

    def __repr__(self) -> str:
        return f"<FlashcardDeck(slug={self.slug})>"


class Flashcard(BaseModel):
    """A single flashcard with multilingual front/back content."""

    __tablename__ = "flashcards"

    deck_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("flashcard_decks.id", ondelete="CASCADE"), nullable=False, index=True
    )
    front: Mapped[dict] = mapped_column(JSON, nullable=False)  # {"en": "...", "hi": "..."}
    back: Mapped[dict] = mapped_column(JSON, nullable=False)
    image_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    order_index: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    # ── Relationships ────────────────────────────────────────
    deck = relationship("FlashcardDeck", back_populates="cards")

    def __repr__(self) -> str:
        return f"<Flashcard(id={self.id}, deck={self.deck_id})>"
