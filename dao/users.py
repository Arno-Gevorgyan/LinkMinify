from typing import Self
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from dao.base import BaseDAO
from db.models import UserModel


class UserDAO(BaseDAO[UserModel]):
    def __init__(self: Self, session: AsyncSession) -> None:
        super().__init__(UserModel, session)

    async def get(
            self: Self, uuid: UUID | None = None, email: str | None = None
    ) -> UserModel:
        """User getting by uuid or email"""

        if uuid:
            query = await self.session.execute(
                select(self.model).where(self.model.uuid == uuid)
            )
        else:
            query = await self.session.execute(
                select(self.model).where(self.model.email == email)
            )

        return query.scalar_one_or_none()
