from pydantic.networks import HttpUrl

from schemas.base import BaseSchema


class LinkCreateRequest(BaseSchema):
    full_url: HttpUrl


class LinkCreateResponse(BaseSchema):
    short_url: str
