import sys
from functools import lru_cache

from pydantic import BaseSettings


class AppConfig(BaseSettings):
    app_name: str = "Link Minify Backend"
    admin_email: str = "admin@linkminify.com"
    environment: str = "local"
    front_end_url: str = "http://127.0.0.1/"
    python_version: str = str(sys.version_info)

    class Config:
        env_file = ".env"


class DBConfig(BaseSettings):
    host: str = "127.0.0.1"
    port: int = 5432
    database: str = "link_minify"
    database_test: str = f"{database}_test"
    username: str = "postgres"
    password: str = "password"

    @property
    def url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.username}:{self.password}"
            f"@{self.host}:{self.port}/{self.database}"
        )

    @property
    def test_url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.username}:{self.password}"
            f"@{self.host}:{self.port}/{self.database_test}"
        )

    @property
    def test_url_sync(self) -> str:
        return self.test_url.replace("+asyncpg", "")

    @property
    def alembic_url(self) -> str:
        return self.url.replace("+asyncpg", "")

    class Config:
        env_file = ".env"
        env_prefix = "db_"


class JWTConfig(BaseSettings):
    secret: str = "some_secret"
    algorithm: str = "HS256"
    header: str = "Bearer"
    expire_minutes: int = 8640  # 6 days
    expire_days: int = 30

    class Config:
        env_file = ".env"
        env_prefix = "jwt_"


class Config(BaseSettings):
    app: AppConfig
    db: DBConfig
    jwt: JWTConfig


@lru_cache
def get_config() -> Config:
    return Config(
        app=AppConfig(),
        db=DBConfig(),
        jwt=JWTConfig(),
    )
