from uuid import UUID
from typing import Any, Generic, Self, Type, TypeVar

from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from db.base import Base

Model = TypeVar("Model", Base, Base)


class BaseDAO(Generic[Model]):
    def __init__(
        self: Self, model: Type[Model], session: AsyncSession
    ) -> None:
        self.model = model
        self.session = session

    def _prepare_data(self: Self, data: dict[str, Any]) -> dict:
        """Data preparing for creation/update"""

        return (
            data if isinstance(data, dict) else data.dict(exclude_unset=True)
        )

    async def create(
        self: Self,
        data: dict[str, Any],
    ) -> Model:
        """New record creation"""

        data_dict = self._prepare_data(data=data)
        new_record = self.model(**data_dict)
        self.session.add(new_record)
        await self.session.flush()
        await self.session.refresh(new_record)

        return new_record

    async def get(self: Self, uuid: UUID) -> Model:
        """Object getting by uuid"""

        query = await self.session.execute(
            select(self.model).where(self.model.uuid == uuid)
        )
        return query.scalar_one_or_none()

    async def get_all(self: Self) -> list[Model]:
        """All objects getting"""

        query = await self.session.execute(select(self.model))
        return query.scalars().unique().all()

    async def update(
        self: Self,
        uuid: UUID,
        data: dict[str, Any],
    ) -> Model:
        """Object updating"""

        data_dict = self._prepare_data(data=data)
        stmt = (
            update(self.model)
            .where(self.model.uuid == uuid)
            .values(**data_dict)
        )
        await self.session.execute(stmt)

        updated_object = await self.session.execute(
            select(self.model).where(self.model.uuid == uuid)
        )
        await self.session.flush()

        return updated_object.scalar_one()

    async def delete(self: Self, uuid: UUID) -> bool:
        """Object deletion"""

        await self.session.execute(
            delete(self.model).where(self.model.uuid == uuid)
        )
        await self.session.flush()
        return True
