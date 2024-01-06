from uuid import UUID

from pydantic import EmailStr

from schemas.base import BaseSchema


class LoginInput(BaseSchema):
    email: str
    password: str | None


class UserInput(BaseSchema):
    first_name: str | None
    last_name: str | None
    email: EmailStr | None


class UserType(UserInput):
    uuid: UUID | None
    is_active: bool | None


class RefreshTokenInput(BaseSchema):
    refresh_token: str


class LoginSuccess(BaseSchema):
    user: UserType
    access_token: str
    refresh_token: str
