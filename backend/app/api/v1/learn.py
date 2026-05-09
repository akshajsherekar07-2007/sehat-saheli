"""
Learn (health education) API — categories and articles.
"""

from fastapi import APIRouter, HTTPException
from sqlalchemy import func, select

from app.core.dependencies import DBSession
from app.models.learn import LearnArticle, LearnCategory
from app.schemas.learn import LearnArticleOut, LearnCategoryOut

router = APIRouter(prefix="/learn", tags=["learn"])


@router.get("/categories", response_model=list[LearnCategoryOut])
async def list_categories(db: DBSession):
    """List all learning categories with article counts."""
    result = await db.execute(
        select(
            LearnCategory,
            func.count(LearnArticle.id).label("article_count"),
        )
        .outerjoin(LearnArticle, LearnArticle.category_id == LearnCategory.id)
        .group_by(LearnCategory.id)
        .order_by(LearnCategory.order_index)
    )
    rows = result.all()
    return [
        LearnCategoryOut(
            id=cat.id, name=cat.name, slug=cat.slug,
            icon=cat.icon, order_index=cat.order_index,
            article_count=count,
        )
        for cat, count in rows
    ]


@router.get("/category/{slug}", response_model=list[LearnArticleOut])
async def get_articles(slug: str, db: DBSession):
    """Get all articles in a category."""
    result = await db.execute(
        select(LearnArticle)
        .join(LearnCategory, LearnArticle.category_id == LearnCategory.id)
        .where(LearnCategory.slug == slug)
        .order_by(LearnArticle.order_index)
    )
    return result.scalars().all()


@router.get("/articles/{article_id}", response_model=LearnArticleOut)
async def get_article(article_id: str, db: DBSession):
    """Get a single article by ID."""
    result = await db.execute(select(LearnArticle).where(LearnArticle.id == article_id))
    article = result.scalar_one_or_none()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    return article
