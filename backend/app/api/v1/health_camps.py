"""
Health Camps API — list, filter, and view government health camps.
"""

from datetime import date

from fastapi import APIRouter
from sqlalchemy import select

from app.core.dependencies import CurrentUserId, DBSession
from app.models.health_camp import HealthCamp
from app.schemas.health_camp import HealthCampOut

router = APIRouter(prefix="/health-camps", tags=["health-camps"])


@router.get("", response_model=list[HealthCampOut])
async def list_camps(
    db: DBSession,
    _user_id: CurrentUserId,
    state: str | None = None,
    district: str | None = None,
    upcoming: bool = True,
):
    """List health camps with optional filters."""
    query = select(HealthCamp).where(HealthCamp.is_active == True)

    if upcoming:
        query = query.where(HealthCamp.event_date >= date.today())
    if state:
        query = query.where(HealthCamp.state.ilike(f"%{state}%"))
    if district:
        query = query.where(HealthCamp.district.ilike(f"%{district}%"))

    query = query.order_by(HealthCamp.event_date.asc())
    result = await db.execute(query)
    return result.scalars().all()


@router.get("/{camp_id}", response_model=HealthCampOut)
async def get_camp(camp_id: str, db: DBSession, _user_id: CurrentUserId):
    """Get details of a specific health camp."""
    from fastapi import HTTPException
    result = await db.execute(select(HealthCamp).where(HealthCamp.id == camp_id))
    camp = result.scalar_one_or_none()
    if not camp:
        raise HTTPException(status_code=404, detail="Health camp not found")
    return camp
