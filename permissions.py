from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.session import get_async_session
from exceptions import NotAuthenticated
from services.users import get_current_user, oauth2_scheme


async def is_admin(
    session: AsyncSession = Depends(get_async_session),
    token: str = Depends(oauth2_scheme),
):
    """Admin permission"""

    user = await get_current_user(session, token)
    if user.is_superuser:
        return user
    raise NotAuthenticated
