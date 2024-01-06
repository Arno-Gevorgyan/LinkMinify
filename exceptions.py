from typing import Any, Self

from fastapi import HTTPException, status

from messages import ErrorMessages
from settings import get_config


class DetailedHTTPException(HTTPException):
    STATUS_CODE = status.HTTP_500_INTERNAL_SERVER_ERROR
    DETAIL = "Server error"

    def __init__(self: Self, **kwargs: dict[str, Any]) -> None:
        super().__init__(
            status_code=self.STATUS_CODE, detail=self.DETAIL, **kwargs
        )


class NotAuthenticated(DetailedHTTPException):
    STATUS_CODE = status.HTTP_401_UNAUTHORIZED
    DETAIL = "Not authenticated"

    def __init__(self: Self) -> None:
        super().__init__(headers={"WWW-Authenticate": get_config().jwt.header})


class BadRequest(DetailedHTTPException):
    STATUS_CODE = status.HTTP_400_BAD_REQUEST
    DETAIL = "Bad Request"


class PermissionDenied(DetailedHTTPException):
    STATUS_CODE = status.HTTP_403_FORBIDDEN
    DETAIL = "Permission denied"


class NotFound(DetailedHTTPException):
    STATUS_CODE = status.HTTP_404_NOT_FOUND
    DETAIL = "Object not found"


class MethodNotAllowed(DetailedHTTPException):
    STATUS_CODE = status.HTTP_405_METHOD_NOT_ALLOWED
    DETAIL = "Method not allowed"


class UnsupportedMediaType(DetailedHTTPException):
    STATUS_CODE = status.HTTP_415_UNSUPPORTED_MEDIA_TYPE
    DETAIL = "This media type is not supported to upload"


class WrongData(DetailedHTTPException):
    STATUS_CODE = status.HTTP_422_UNPROCESSABLE_ENTITY


class ExpiredJWT(NotAuthenticated):
    DETAIL = "Expired JWT"


class InvalidJWT(NotAuthenticated):
    DETAIL = "Invalid JWT"


class WrongJWTType(NotAuthenticated):
    DETAIL = "Wrong JWT type"


class UserNotFound(NotFound):
    DETAIL = ErrorMessages.USER_NOT_EXISTS


class EmailUsed(WrongData):
    DETAIL = ErrorMessages.USER_EXISTS_EMAIL


class EmailIncorrect(WrongData):
    DETAIL = ErrorMessages.INCORRECT_EMAIL


class UrlIncorrect(WrongData):
    DETAIL = ErrorMessages.NOT_A_VALID_URL


class SHORT_URL_NOT_FOUND(NotFound):
    DETAIL = ErrorMessages.SHORT_URL_NOT_FOUND
