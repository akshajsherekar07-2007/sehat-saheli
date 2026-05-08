"""
Quiz API — categories, questions, and attempt tracking.
"""

import uuid
from datetime import date

from fastapi import APIRouter, HTTPException
from sqlalchemy import Integer, func, select

from app.core.dependencies import CurrentUserId, DBSession
from app.models.quiz import Quiz, QuizAttempt, QuizCategory
from app.schemas.quiz import (
    QuizAttemptCreate,
    QuizAttemptOut,
    QuizCategoryOut,
    QuizOut,
    QuizResultOut,
    QuizStatsOut,
)

router = APIRouter(prefix="/quiz", tags=["quiz"])


@router.get("/categories", response_model=list[QuizCategoryOut])
async def list_categories(db: DBSession, _user_id: CurrentUserId):
    """List all quiz categories with question counts."""
    result = await db.execute(
        select(
            QuizCategory,
            func.count(Quiz.id).label("quiz_count"),
        )
        .outerjoin(Quiz, Quiz.category_id == QuizCategory.id)
        .group_by(QuizCategory.id)
        .order_by(QuizCategory.name)
    )
    rows = result.all()
    return [
        QuizCategoryOut(
            id=cat.id, name=cat.name, slug=cat.slug,
            description=cat.description, image_url=cat.image_url,
            quiz_count=count,
        )
        for cat, count in rows
    ]


@router.get("/category/{slug}", response_model=list[QuizOut])
async def get_quizzes_by_category(slug: str, db: DBSession, _user_id: CurrentUserId):
    """Get all quizzes in a category (without answers)."""
    result = await db.execute(
        select(Quiz)
        .join(QuizCategory, Quiz.category_id == QuizCategory.id)
        .where(QuizCategory.slug == slug)
    )
    return result.scalars().all()


@router.get("/daily", response_model=list[QuizOut])
async def get_daily_quiz(db: DBSession, _user_id: CurrentUserId):
    """Get today's daily quiz questions."""
    today = date.today()
    result = await db.execute(
        select(Quiz).where(Quiz.is_daily == True, Quiz.daily_date == today)
    )
    quizzes = result.scalars().all()
    if not quizzes:
        # Fallback: get any 5 random quizzes
        result = await db.execute(select(Quiz).limit(5))
        quizzes = result.scalars().all()
    return quizzes


@router.post("/{quiz_id}/attempt", response_model=QuizResultOut)
async def submit_attempt(
    quiz_id: str, body: QuizAttemptCreate, db: DBSession, user_id: CurrentUserId
):
    """Submit an answer for a quiz question."""
    result = await db.execute(select(Quiz).where(Quiz.id == quiz_id))
    quiz = result.scalar_one_or_none()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")

    is_correct = body.selected_option == quiz.correct_option
    score = 10 if is_correct else 0

    attempt = QuizAttempt(
        id=str(uuid.uuid4()),
        user_id=user_id,
        quiz_id=quiz_id,
        selected_option=body.selected_option,
        is_correct=is_correct,
        score=score,
    )
    db.add(attempt)
    await db.commit()
    await db.refresh(attempt)

    return QuizResultOut(
        attempt=QuizAttemptOut.model_validate(attempt),
        correct_option=quiz.correct_option,
    )


@router.get("/stats", response_model=QuizStatsOut)
async def get_stats(db: DBSession, user_id: CurrentUserId):
    """Get the current user's quiz statistics."""
    result = await db.execute(
        select(
            func.count(QuizAttempt.id),
            func.coalesce(func.sum(func.cast(QuizAttempt.is_correct, Integer)), 0),
            func.coalesce(func.sum(QuizAttempt.score), 0),
        ).where(QuizAttempt.user_id == user_id)
    )
    row = result.one()
    total = row[0] or 0
    correct = row[1] or 0
    score = row[2] or 0
    return QuizStatsOut(
        total_attempts=total,
        correct_count=correct,
        total_score=score,
        accuracy=round(correct / total * 100, 1) if total > 0 else 0.0,
    )
