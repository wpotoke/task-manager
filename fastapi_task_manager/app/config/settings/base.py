import pathlib

import pydantic_settings
from pydantic_settings import SettingsConfigDict

ROOT_DIR: pathlib.Path = pathlib.Path(
    __file__
).parent.parent.parent.parent.parent.resolve()


class BaseConfig(pydantic_settings.BaseSettings):
    model_config = SettingsConfigDict(
        env_file=ROOT_DIR / ".env", env_file_encoding="utf-8", extra="ignore"
    )


class BackendBaseSettings(BaseConfig):
    model_config = SettingsConfigDict(env_prefix="fastAPI_")

    DESCRIPTION: str | None = None
    TIMEZONE: str = "UTC"
    DEBUG: bool = False

    BACKEND_SERVER_HOST: str
    BACKEND_SERVER_PORT: int
    POSTGRES_HOST: str
    POSTGRES_DB: str
    POSTGRES_PASSWORD: str
    POSTGRES_PORT: str
    POSTGRES_USERNAME: str
    POSTGRES_SCHEMA: str
    IS_DB_ECHO_LOG: str
    DB_POOL_OVERFLOW: int
    DB_POOL_SIZE: int
