from typing import Self
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import UserModel
from dao.base import BaseDAO


class UserDAO(BaseDAO[UserModel]):
    def __init__(self: Self, session: AsyncSession) -> None:
        super().__init__(UserModel, session)

    async def get(
            self: Self, uuid: UUID | None = None, email: str | None = None
    ) -> UserModel:
        """User getting by uuid or email"""

        if uuid:
            query = await self.session.execute(
                select(UserModel).where(UserModel.uuid == uuid)
            )
        else:
            query = await self.session.execute(
                select(UserModel).where(UserModel.email == email)
            )

        return query.scalar_one_or_none()
