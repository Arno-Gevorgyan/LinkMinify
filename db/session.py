from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from settings import get_config


class Engine:
    db_url: str = get_config().db.url

    @classmethod
    def get(cls) -> AsyncEngine:
        return create_async_engine(
            cls.db_url,
            pool_size=20,
            pool_pre_ping=True,
            pool_use_lifo=True,
            echo=False,
        )

    @classmethod
    def set(cls, db_url: str | None = None) -> str:
        if db_url:
            cls.db_url = db_url
        return cls.db_url


async_session_factory = async_sessionmaker(
    bind=Engine.get(),
    autoflush=False,
    expire_on_commit=False,
)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_factory.begin() as session:
        yield session
