import random

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from dao.links import LinkDAO
from db.session import get_async_session
from exceptions import SHORT_URL_NOT_FOUND, UrlIncorrect
from schemas.links import LinkCreateRequest, LinkCreateResponse
from services.utils import generate_short_url

from services.validators import is_reachable_url, is_valid_url


async def short_link_create(request: LinkCreateRequest,
                            session: AsyncSession = Depends(get_async_session)) -> LinkCreateResponse:

    full_url = request.full_url.strip()
    if not is_valid_url(full_url) or not is_reachable_url(full_url):
        raise UrlIncorrect

    existing_link = await LinkDAO(session).get_by_url(full_url=full_url)
    if existing_link:
        return LinkCreateResponse(short_url=existing_link.short_url)

    # Attempt to generate a unique short URL
    short_url = generate_short_url(full_url)
    existing_short_link = await LinkDAO(session).get_by_url(short_url=short_url)

    # Keep generating new short URLs until a unique one is found
    while existing_short_link:
        # Modify the URL with a random number to get a new hash
        modified_url = f"{request.full_url}{random.randint(1, 10000)}"
        short_url = generate_short_url(modified_url)
        existing_short_link = await LinkDAO(session).get_by_url(short_url=short_url)

    await LinkDAO(session).create(data={"short_url": short_url, "full_url": full_url})
    await session.commit()
    return LinkCreateResponse(short_url=short_url)


async def delete_link_from_db(short_url: str, session: AsyncSession = Depends(get_async_session)) -> dict:
    deleted_count = await LinkDAO(session).delete_by_short_url(short_url.strip())

    if deleted_count == 0:
        raise SHORT_URL_NOT_FOUND
    return {"message": f"Short URL {short_url} successfully deleted"}


async def full_url_redirect(short_url: str, session: AsyncSession = Depends(get_async_session)) -> dict:
    link = await LinkDAO(session).get_by_url(short_url=short_url.strip())

    if link is None:
        raise SHORT_URL_NOT_FOUND
    return {"redirect_url": link.full_url}
