"""
Generic base repository providing CRUD operations for any SQLAlchemy model.
All feature-specific repositories extend this to inherit standard operations
and add custom queries as needed.

This is the core reusability abstraction for the data access layer.
"""

from typing import Any, Generic, Sequence, Type, TypeVar

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.base import BaseModel

ModelType = TypeVar("ModelType", bound=BaseModel)


class BaseRepository(Generic[ModelType]):
    """
    Generic async CRUD repository.
    
    Usage:
        class UserRepo(BaseRepository[User]):
            def __init__(self, session: AsyncSession):
                super().__init__(User, session)
    """

    def __init__(self, model: Type[ModelType], session: AsyncSession) -> None:
        self._model = model
        self._session = session

    async def get_by_id(self, entity_id: str) -> ModelType | None:
        """Fetch a single entity by primary key."""
        return await self._session.get(self._model, entity_id)

    async def get_all(
        self,
        *,
        skip: int = 0,
        limit: int = 50,
        order_by: Any = None,
    ) -> Sequence[ModelType]:
        """Fetch a paginated list of entities."""
        stmt = select(self._model)
        if order_by is not None:
            stmt = stmt.order_by(order_by)
        else:
            stmt = stmt.order_by(self._model.created_at.desc())
        stmt = stmt.offset(skip).limit(limit)
        result = await self._session.execute(stmt)
        return result.scalars().all()

    async def count(self) -> int:
        """Count total entities of this model type."""
        stmt = select(func.count()).select_from(self._model)
        result = await self._session.execute(stmt)
        return result.scalar_one()

    async def create(self, entity: ModelType) -> ModelType:
        """Insert a new entity and flush to get the generated ID."""
        self._session.add(entity)
        await self._session.flush()
        await self._session.refresh(entity)
        return entity

    async def create_many(self, entities: list[ModelType]) -> list[ModelType]:
        """Bulk insert multiple entities."""
        self._session.add_all(entities)
        await self._session.flush()
        for entity in entities:
            await self._session.refresh(entity)
        return entities

    async def update(self, entity: ModelType, update_data: dict) -> ModelType:
        """Update an entity with a partial dictionary of changes."""
        for field, value in update_data.items():
            if hasattr(entity, field) and value is not None:
                setattr(entity, field, value)
        await self._session.flush()
        await self._session.refresh(entity)
        return entity

    async def delete(self, entity: ModelType) -> None:
        """Delete an entity."""
        await self._session.delete(entity)
        await self._session.flush()

    async def delete_by_id(self, entity_id: str) -> bool:
        """Delete an entity by ID. Returns True if found and deleted."""
        entity = await self.get_by_id(entity_id)
        if entity:
            await self.delete(entity)
            return True
        return False

    async def exists(self, entity_id: str) -> bool:
        """Check if an entity exists by ID."""
        entity = await self.get_by_id(entity_id)
        return entity is not None

    async def get_by_field(self, field_name: str, value: Any) -> ModelType | None:
        """Fetch a single entity by an arbitrary field value."""
        column = getattr(self._model, field_name, None)
        if column is None:
            raise ValueError(f"Model {self._model.__name__} has no field '{field_name}'")
        stmt = select(self._model).where(column == value)
        result = await self._session.execute(stmt)
        return result.scalars().first()

    async def filter_by(
        self,
        *,
        skip: int = 0,
        limit: int = 50,
        **filters: Any,
    ) -> Sequence[ModelType]:
        """Fetch entities matching keyword-argument filters."""
        stmt = select(self._model)
        for field, value in filters.items():
            column = getattr(self._model, field, None)
            if column is not None and value is not None:
                stmt = stmt.where(column == value)
        stmt = stmt.order_by(self._model.created_at.desc()).offset(skip).limit(limit)
        result = await self._session.execute(stmt)
        return result.scalars().all()
