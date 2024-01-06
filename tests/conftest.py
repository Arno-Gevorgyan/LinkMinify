import asyncio
import os
from datetime import timedelta
from contextlib import contextmanager
from typing import AsyncGenerator, Callable, Generator

import pytest
import uuid6  # noqa
from yarl import URL
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy import create_engine
from sqlalchemy_utils import create_database, drop_database  # noqa
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from dao.users import UserDAO
from settings import get_config
from db.models import UserModel
from services.users import get_user
from alembic.command import downgrade
from utils.auth import create_jwt_token
from db.session import async_session_factory
from tests.test_migration import alembic_config_from_url

pytestmark = pytest.mark.asyncio  # for running async tests


@contextmanager
def tmp_database(db_url: URL, suffix: str = "", **kwargs):  # noqa
    yield get_config().db.test_url_sync


@pytest.fixture(scope="session")
def pg_url():
    """
    Provides base PostgreSQL URL for creating temporary databases.
    """
    return URL(os.getenv("CI_STAFF_PG_URL", get_config().db.test_url_sync))


@pytest.fixture()
def postgres(pg_url):
    """
    Creates empty temporary database.
    """
    with tmp_database(pg_url, "pytest") as tmp_url:
        yield tmp_url


@pytest.fixture()
def postgres_engine(postgres):
    """
    SQLAlchemy engine, bound to temporary database.
    """
    engine = create_engine(postgres, echo=True)
    try:
        yield engine
    finally:
        engine.dispose()


@pytest.fixture()
def alembic_config(postgres):
    """
    Alembic configuration object, bound to temporary database.
    """
    return alembic_config_from_url(postgres)


@pytest.fixture()
async def get_engine():
    engine = create_async_engine(get_config().db.test_url)
    yield engine
    await engine.dispose()


@pytest.fixture(scope="session")
def event_loop(request) -> Generator:
    """Create an instance of the default event loop for each test case"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

    def fin():
        """Downgrade db after all tests"""
        alembic_config = alembic_config_from_url(get_config().db.test_url_sync)
        downgrade(alembic_config, "base")

    request.addfinalizer(fin)


@pytest.fixture()
async def db_session(get_engine) -> AsyncSession:
    async with get_engine.begin() as connection:
        async with async_session_factory(bind=connection) as session:
            yield session
            await session.close()


@pytest.fixture()
def override_get_async_session(db_session: AsyncSession) -> Callable:
    async def _override_get_async_session():
        yield db_session

    return _override_get_async_session


@pytest.fixture()
def app(override_get_async_session: Callable) -> FastAPI:
    from db.session import get_async_session
    from main import app

    app.dependency_overrides[get_async_session] = override_get_async_session
    return app


@pytest.fixture()
async def async_client(app: FastAPI) -> AsyncGenerator:
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.fixture()
async def session(get_engine) -> AsyncSession:
    async with get_engine.begin() as connection:
        async with async_session_factory(bind=connection) as session:
            yield session
            await session.close()


@pytest.fixture()
async def async_client_auth(app: FastAPI, head) -> AsyncGenerator:
    async with AsyncClient(
            app=app, base_url="http://test", headers=head
    ) as ac:
        yield ac


@pytest.fixture()
async def auth_token(user: UserModel) -> dict:
    return create_jwt_token(
        data={"token_type": "access", "user_id": str(user.uuid)},
        expires_delta=timedelta(minutes=get_config().jwt.expire_minutes),
    )


@pytest.fixture()
async def head(auth_token: str) -> dict:
    return {"Authorization": f"{get_config().jwt.header} {auth_token}"}


@pytest.fixture()
async def user(session: AsyncSession) -> UserModel:
    email = "test@gmail.com"
    if not (
            user := await get_user(
                session=session, email=email
            )
    ):
        user = await UserDAO(session).create(data={"email": email})

    return user