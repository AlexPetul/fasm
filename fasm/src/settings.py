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

    aws_cognito_region: str
    aws_access_key_id: SecretStr
    aws_secret_access_key: SecretStr
    aws_cognito_client_id: SecretStr
    aws_cognito_user_pool: SecretStr

    openai_api_key: SecretStr

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
