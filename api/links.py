from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.session import get_async_session
from schemas.links import LinkCreateRequest, LinkCreateResponse
from services.links import delete_link_from_db, full_url_redirect, short_link_create

link_router = APIRouter()


@link_router.post("/create-short-link")
async def create_short_link(request: LinkCreateRequest,
                            session: AsyncSession = Depends(get_async_session)) -> LinkCreateResponse:
    """
    Creates a new short link for a given full URL.

    This endpoint first validates the given URL to ensure it's well-formed and reachable.
    If the URL is already in the database, the existing short URL is returned.
    Otherwise, a unique short URL is generated. In case of a collision (the generated short URL
    already exists), the function will keep generating a new URL until a unique one is found.

    Args:
        request (LinkCreateRequest): The request object containing the full URL to be shortened.
        session (AsyncSession): The database session dependency, injected by FastAPI.

    Raises:
        UrlIncorrect: If the provided URL is invalid or unreachable.

    Returns:
        LinkCreateResponse: The response object containing the generated short URL.
    """
    return await short_link_create(request, session)


@link_router.delete("/delete-link/")
async def delete_link(short_url: str, session: AsyncSession = Depends(get_async_session)) -> dict:
    """
    Deletes a given short link.

    Args:
        short_url (str): The short URL to be deleted.
        session (AsyncSession): Database session dependency.

    Returns:
        dict: A message indicating the operation status.
    """

    return await delete_link_from_db(short_url, session)


@link_router.get("/redirect/")
async def redirect_to_full_url(short_url: str, session: AsyncSession = Depends(get_async_session)) -> dict:
    """
    Redirects to the full URL corresponding to the given short URL.

    Args:
        short_url (str): The short URL to redirect from.
        session (AsyncSession): Database session dependency.

    Returns:
        dict: with value redirect url.
    """
    return await full_url_redirect(short_url, session)
