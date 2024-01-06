from datetime import timedelta
from uuid import UUID

from fastapi import Depends, status
from starlette.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordBearer

from dao.users import UserDAO
from db.models import UserModel
from settings import get_config
from schemas.base import MessageType
from db.session import get_async_session
from exceptions import PermissionDenied, UserNotFound, EmailUsed
from schemas.users import LoginInput, LoginSuccess, RefreshTokenInput, UserType
from utils.auth import create_jwt_token, decode_token, verify_password, hash_password

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
optional_oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="token", auto_error=False
)


def get_login_data(user: UserModel) -> LoginSuccess:
    """Returning user with access, refresh, firebase and ws tokens"""

    access_token = create_jwt_token(
        data={"token_type": "access", "user_uuid": str(user.uuid)},
        expires_delta=timedelta(minutes=get_config().jwt.expire_minutes),
    )
    refresh_token = create_jwt_token(
        data={"token_type": "refresh", "user_uuid": str(user.uuid)},
        expires_delta=timedelta(days=get_config().jwt.expire_days),
    )

    return LoginSuccess(
        user=user,
        access_token=access_token,
        refresh_token=refresh_token,
    )


async def token_refresh(
        data: RefreshTokenInput,
        session: AsyncSession,
) -> LoginSuccess:
    user_uuid = decode_token(token=data.refresh_token)
    if user := await get_user(session=session, user_uuid=user_uuid) is None:
        raise UserNotFound

    return get_login_data(user=user)


async def user_from_token(
        token: str, session: AsyncSession
) -> UserModel:
    user_uuid = decode_token(token=token)

    if not (user := await UserDAO(session).get(uuid=user_uuid)):
        raise UserNotFound
    return user


async def get_current_user(
        session: AsyncSession = Depends(get_async_session),
        token: str = Depends(oauth2_scheme),
) -> UserModel:
    """Getting current user by token"""
    return await user_from_token(
        token=token, session=session
    )


async def get_user(
        session: AsyncSession,
        email: str = None,
        user_uuid: UUID = None,
) -> UserModel | None:
    """Getting user by email, phone number or id"""

    if user_uuid:
        user = await UserDAO(session).get(uuid=user_uuid)
    elif email:
        user = await UserDAO(session).get(email=email)
    else:
        return None
    return user


async def create_user(
        data: LoginInput, session: AsyncSession
) -> JSONResponse:
    """User creation by phone number"""

    if await UserDAO(session).get(email=data.email):
        raise EmailUsed
    password = hash_password(data.password)
    user = await UserDAO(session).create(data={"email": data.email, 'is_active': True, 'hashed_password': password})
    await session.commit()
    return JSONResponse(
        content=jsonable_encoder(UserType.from_orm(user)),
        status_code=status.HTTP_201_CREATED,
    )


async def login_user(data: LoginInput, session: AsyncSession) -> LoginSuccess:
    """User authentication"""

    user = await get_user(session, email=data.email)
    if not user:
        raise UserNotFound

    return get_login_data(user=user)


async def login_admin(data: LoginInput, session: AsyncSession) -> str:
    """User authentication: admin panel"""

    user = await UserDAO(session).get(email=data.email.lower())
    if not user:
        raise UserNotFound()
    if (
            not verify_password(data.password, user.hashed_password)
            or not user.is_active
    ):
        raise PermissionDenied()

    return create_jwt_token(
        data={"token_type": "access", "user_uuid": str(user.uuid)},
        expires_delta=timedelta(minutes=get_config().jwt.expire_minutes),
    )


async def delete_user(
        user: UserModel, session: AsyncSession
) -> MessageType:
    """User deletion"""

    await UserDAO(session).delete(uuid=user.uuid)

    return MessageType(detail=f"User {user.email} was deleted")
