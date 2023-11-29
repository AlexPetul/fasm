from functools import lru_cache

from pydantic import SecretStr
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    aws_cognito_region: str
    aws_access_key_id: SecretStr
    aws_secret_access_key: SecretStr
    aws_cognito_client_id: SecretStr
    aws_cognito_user_pool: SecretStr

    openai_api_key: SecretStr


@lru_cache
def get_settings():
    return Settings()
