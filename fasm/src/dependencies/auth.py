from functools import cache
from typing import (
    Dict,
    List,
)

import jwt.exceptions
import requests
from fastapi import (
    Depends,
    HTTPException,
    status,
)
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
)
from jose import (
    jwk,
    jwt,
)
from jose.utils import base64url_decode

from src.auth.models import User
from src.auth.repository import UsersRepository
from src.auth.token import decode_jwt_token
from src.dependencies.database import get_repository
from src.settings import get_settings, Settings


async def get_current_user(
    token: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
    user_repository: UsersRepository = Depends(get_repository(UsersRepository)),
    settings: Settings = Depends(get_settings),
) -> User:
    try:
        payload = decode_jwt_token(token.credentials, settings.access_token_secret_key.get_secret_value())

        if (username := payload.get("username")) is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")

        if (user := await user_repository.get_by_username(username)) is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")

        return user

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")
