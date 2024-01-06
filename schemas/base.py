from typing import TypeVar

from fastapi_camelcase import CamelModel


class BaseSchema(CamelModel):
    class Config:
        orm_mode = True


class MessageType(BaseSchema):
    detail: str | list


Schema = TypeVar("Schema", bound=BaseSchema)
