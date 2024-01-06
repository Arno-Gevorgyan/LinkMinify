from schemas.base import BaseSchema


class LinkCreateRequest(BaseSchema):
    full_url: str


class LinkCreateResponse(BaseSchema):
    short_url: str
