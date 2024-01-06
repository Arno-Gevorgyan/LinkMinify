from starlette.responses import JSONResponse
from pydantic.networks import validate_email
from fastapi.encoders import jsonable_encoder
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import UserModel
from schemas.base import MessageType
from utils.auth import verify_password
from db.session import get_async_session
from exceptions import EmailIncorrect, PermissionDenied
from schemas.users import LoginSuccess, RefreshTokenInput, UserType, LoginInput
from services.users import delete_user, get_current_user, token_refresh, get_user, create_user

auth_router = APIRouter()
user_router = APIRouter()


@auth_router.post("/token/refresh")
async def refresh_token(
        data: RefreshTokenInput, session: AsyncSession = Depends(get_async_session)
) -> LoginSuccess:
    """Getting new access and refresh tokens"""

    return await token_refresh(data=data, session=session)


@auth_router.post(
    "/login",
    responses={
        201: {
            "description": "Successful Response when user was created",
            "content": {
                "application/json": {
                    "schema": {"$ref": "#/components/schemas/UserType"}
                }
            },
        }
    },
)
async def user_create(
        data: LoginInput,
        session: AsyncSession = Depends(get_async_session),
) -> JSONResponse:
    """New user creation or login by email"""

    if user := await get_user(session=session, email=data.email):
        if not verify_password(data.password, user.hashed_password):
            raise PermissionDenied
        return JSONResponse(
            content=jsonable_encoder(UserType.from_orm(user)),
            status_code=status.HTTP_200_OK,
        )
    try:
        validate_email(data.email)
    except Exception:
        raise EmailIncorrect
    return await create_user(data, session)


@user_router.get("/me")
async def me(
        current_user: UserType = Depends(get_current_user),
) -> UserType:
    """Getting current user"""

    return current_user


@user_router.delete("/me")
async def user_delete(
        current_user: UserModel = Depends(get_current_user),
        session: AsyncSession = Depends(get_async_session),
) -> MessageType:
    """User deletion"""

    return await delete_user(current_user, session)
