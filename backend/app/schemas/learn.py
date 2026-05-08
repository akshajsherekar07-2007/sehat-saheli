"""
Learn (health education) Pydantic schemas.
"""

from pydantic import BaseModel


class LearnCategoryOut(BaseModel):
    id: str
    name: str
    slug: str
    icon: str | None = None
    order_index: int = 0
    article_count: int = 0

    model_config = {"from_attributes": True}


class LearnArticleOut(BaseModel):
    id: str
    category_id: str
    title: dict
    content: dict
    image_url: str | None = None
    video_url: str | None = None
    content_type: str = "article"
    order_index: int = 0

    model_config = {"from_attributes": True}
