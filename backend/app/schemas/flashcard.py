"""
Flashcard Pydantic schemas.
"""

from pydantic import BaseModel


class FlashcardDeckOut(BaseModel):
    id: str
    name: str
    slug: str
    description: str | None = None
    image_url: str | None = None
    category: str
    card_count: int = 0

    model_config = {"from_attributes": True}


class FlashcardOut(BaseModel):
    id: str
    deck_id: str
    front: dict
    back: dict
    image_url: str | None = None
    order_index: int = 0

    model_config = {"from_attributes": True}
