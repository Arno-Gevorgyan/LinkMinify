from uuid import UUID
from datetime import datetime, timedelta

from passlib.context import CryptContext
from jose import ExpiredSignatureError, JWTError, jwt

from settings import get_config
from exceptions import ExpiredJWT, InvalidJWT, UserNotFound, WrongJWTType

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception:
        return False


def create_jwt_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode["exp"] = expire

    return jwt.encode(
        to_encode,
        get_config().jwt.secret,
        algorithm=get_config().jwt.algorithm,
    )


def decode_token(token: str) -> str:
    try:
        payload = jwt.decode(
            token,
            get_config().jwt.secret,
            algorithms=[get_config().jwt.algorithm],
        )
        user_uuid: str = payload.get("user_uuid")
        token_type: str = payload.get("token_type")
        if user_uuid is None:
            raise UserNotFound
        if token_type != "access":
            raise WrongJWTType
    except ExpiredSignatureError as e:
        raise ExpiredJWT from e
    except JWTError as e:
        raise InvalidJWT from e
    return user_uuid


def hash_password(password: str) -> str:
    """Hash a password for storing."""
    return pwd_context.hash(password)
