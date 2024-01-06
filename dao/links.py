from typing import Self

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from dao.base import BaseDAO
from db.models import ShortLinkModel


class LinkDAO(BaseDAO[ShortLinkModel]):
    def __init__(self: Self, session: AsyncSession) -> None:
        super().__init__(ShortLinkModel, session)

    async def get(
            self: Self, full_url: str | None = None, short_url: str | None = None
    ) -> ShortLinkModel:
        """Link getting by short or full url"""

        if full_url:
            query = await self.session.execute(
                select(self.model).where(self.model.full_url == full_url)
            )
        else:
            query = await self.session.execute(
                select(self.model).where(self.model.short_url == short_url)
            )

        return query.scalar_one_or_none()
