"""
Dashboard (Cycle Tracking) API — log cycles, predict, get analytics.
"""

import uuid
from datetime import date, timedelta

from fastapi import APIRouter, HTTPException
from sqlalchemy import func, select

from app.core.dependencies import CurrentUserId, DBSession
from app.models.cycle import CycleLog
from app.schemas.dashboard import (
    CycleAnalytics,
    CycleLogCreate,
    CycleLogOut,
    CyclePrediction,
)

router = APIRouter(prefix="/cycles", tags=["dashboard"])


@router.post("", response_model=CycleLogOut)
async def log_cycle(body: CycleLogCreate, db: DBSession, user_id: CurrentUserId):
    """Log a new menstrual cycle entry."""
    log = CycleLog(
        id=str(uuid.uuid4()),
        user_id=user_id,
        period_start=body.period_start,
        period_end=body.period_end,
        cycle_length=body.cycle_length,
        symptoms=body.symptoms,
        notes=body.notes,
    )
    db.add(log)
    await db.commit()
    await db.refresh(log)
    return log


@router.get("", response_model=list[CycleLogOut])
async def list_cycles(
    db: DBSession, user_id: CurrentUserId, skip: int = 0, limit: int = 20
):
    """Get the user's cycle history, most recent first."""
    result = await db.execute(
        select(CycleLog)
        .where(CycleLog.user_id == user_id)
        .order_by(CycleLog.period_start.desc())
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()


@router.delete("/{log_id}")
async def delete_cycle(log_id: str, db: DBSession, user_id: CurrentUserId):
    """Delete a cycle log entry."""
    result = await db.execute(
        select(CycleLog).where(CycleLog.id == log_id, CycleLog.user_id == user_id)
    )
    log = result.scalar_one_or_none()
    if not log:
        raise HTTPException(status_code=404, detail="Cycle log not found")
    await db.delete(log)
    await db.commit()
    return {"detail": "Deleted"}


@router.get("/predict", response_model=CyclePrediction)
async def predict_next(db: DBSession, user_id: CurrentUserId):
    """Predict the next cycle start date based on history."""
    result = await db.execute(
        select(CycleLog)
        .where(CycleLog.user_id == user_id, CycleLog.cycle_length.isnot(None))
        .order_by(CycleLog.period_start.desc())
        .limit(6)
    )
    logs = result.scalars().all()
    if len(logs) < 2:
        raise HTTPException(status_code=400, detail="Need at least 2 cycle entries to predict")

    avg_length = round(sum(l.cycle_length for l in logs) / len(logs))
    last_start = logs[0].period_start
    predicted = last_start + timedelta(days=avg_length)

    return CyclePrediction(
        predicted_start=predicted,
        average_cycle_length=avg_length,
        based_on_entries=len(logs),
    )


@router.get("/analytics", response_model=CycleAnalytics)
async def get_analytics(db: DBSession, user_id: CurrentUserId):
    """Get cycle analytics — averages, min/max."""
    result = await db.execute(
        select(CycleLog)
        .where(CycleLog.user_id == user_id, CycleLog.cycle_length.isnot(None))
    )
    logs = result.scalars().all()

    if not logs:
        return CycleAnalytics()

    lengths = [l.cycle_length for l in logs if l.cycle_length]
    period_lengths = [
        (l.period_end - l.period_start).days + 1
        for l in logs if l.period_end
    ]

    return CycleAnalytics(
        total_logs=len(logs),
        average_cycle_length=round(sum(lengths) / len(lengths), 1) if lengths else 0,
        average_period_length=round(sum(period_lengths) / len(period_lengths), 1) if period_lengths else 0,
        shortest_cycle=min(lengths) if lengths else None,
        longest_cycle=max(lengths) if lengths else None,
    )
