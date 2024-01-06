from typing import Self

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from dao.base import BaseDAO
from db.models import ShortLinkModel, UserShortLinkModel


class UserLinkDAO(BaseDAO[UserShortLinkModel]):
    def __init__(self: Self, session: AsyncSession) -> None:
        super().__init__(UserShortLinkModel, session)


class LinkDAO(BaseDAO[ShortLinkModel]):
    def __init__(self: Self, session: AsyncSession) -> None:
        super().__init__(ShortLinkModel, session)

    async def get_by_url(self: Self, full_url: str | None = None, short_url: str | None = None) -> ShortLinkModel:
        """Link getting by short or full url"""

        if full_url:
            query = await self.session.execute(
                select(self.model).where(ShortLinkModel.full_url == full_url)
            )
        else:
            query = await self.session.execute(
                select(self.model).where(ShortLinkModel.short_url == short_url)
            )

        return query.scalar_one_or_none()

    async def delete_by_short_url(self: Self, short_url: str) -> int:
        """
        Deletes a link by its short URL.

        Args:
            short_url (str): The short URL of the link to be deleted.

        Returns:
            int: The number of rows deleted (0 if not found, 1 if deleted).
        """
        query = delete(ShortLinkModel).where(ShortLinkModel.short_url == short_url)
        result = await self.session.execute(query)
        print(result, 898989)
        await self.session.commit()
        return result.rowcount
