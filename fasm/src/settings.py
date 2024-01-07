from functools import lru_cache

from pydantic import (
    PostgresDsn,
    SecretStr,
)
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    env_file: str = ".env"

    db_user: str
    db_name: str
    db_password: str
    db_host: str = "postgres"
    db_driver: str = "postgresql+asyncpg"

    openai_api_key: SecretStr

    access_token_secret_key: SecretStr
    access_token_expires: int
    refresh_token_secret_key: SecretStr
    refresh_token_expires: int

    @property
    def database_url(self):
        dsn = PostgresDsn.build(
            scheme=self.db_driver,
            host=self.db_host,
            path=self.db_name,
            username=self.db_user,
            password=self.db_password,
        )
        return str(dsn)


@lru_cache
def get_settings():
    return Settings()
