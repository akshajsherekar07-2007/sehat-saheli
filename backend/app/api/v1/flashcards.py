"""
Flashcard API — decks and cards.
"""

from fastapi import APIRouter, HTTPException
from sqlalchemy import func, select

from app.core.dependencies import CurrentUserId, DBSession
from app.models.flashcard import Flashcard, FlashcardDeck
from app.schemas.flashcard import FlashcardDeckOut, FlashcardOut

router = APIRouter(prefix="/flashcards", tags=["flashcards"])


@router.get("/decks", response_model=list[FlashcardDeckOut])
async def list_decks(db: DBSession, _user_id: CurrentUserId):
    """List all flashcard decks with card counts."""
    result = await db.execute(
        select(
            FlashcardDeck,
            func.count(Flashcard.id).label("card_count"),
        )
        .outerjoin(Flashcard, Flashcard.deck_id == FlashcardDeck.id)
        .group_by(FlashcardDeck.id)
        .order_by(FlashcardDeck.name)
    )
    rows = result.all()
    return [
        FlashcardDeckOut(
            id=deck.id, name=deck.name, slug=deck.slug,
            description=deck.description, image_url=deck.image_url,
            category=deck.category, card_count=count,
        )
        for deck, count in rows
    ]


@router.get("/decks/{slug}", response_model=list[FlashcardOut])
async def get_deck_cards(slug: str, db: DBSession, _user_id: CurrentUserId):
    """Get all cards in a deck."""
    result = await db.execute(
        select(Flashcard)
        .join(FlashcardDeck, Flashcard.deck_id == FlashcardDeck.id)
        .where(FlashcardDeck.slug == slug)
        .order_by(Flashcard.order_index)
    )
    cards = result.scalars().all()
    if not cards:
        raise HTTPException(status_code=404, detail="Deck not found or empty")
    return cards
