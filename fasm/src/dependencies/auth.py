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
from src.dependencies.database import get_repository
from src.settings import get_settings


@cache
def get_cognito_public_keys() -> List[Dict]:
    settings = get_settings()

    jwks_url = "https://cognito-idp.{region}.amazonaws.com/{pool}/.well-known/jwks.json".format(
        region=settings.aws_cognito_region,
        pool=settings.aws_cognito_user_pool.get_secret_value(),
    )

    response = requests.get(jwks_url)
    return response.json()["keys"]


def get_issuer() -> str:
    settings = get_settings()
    return "https://cognito-idp.{region}.amazonaws.com/{pool}".format(
        region=settings.aws_cognito_region,
        pool=settings.aws_cognito_user_pool.get_secret_value(),
    )


def verify_token(token, public_keys, issuer):
    headers = jwt.get_unverified_headers(token)
    kid = headers["kid"]

    key_index = -1
    for i in range(len(public_keys)):
        if kid == public_keys[i]["kid"]:
            key_index = i
            break

    if key_index == -1:
        raise Exception("Public key not found in jwks.json")

    public_key = jwk.construct(public_keys[key_index])
    message, encoded_signature = str(token).rsplit(".", 1)
    decoded_signature = base64url_decode(encoded_signature.encode("utf-8"))

    if not public_key.verify(message.encode("utf8"), decoded_signature):
        raise Exception("Signature verification failed")

    claims = jwt.get_unverified_claims(token)
    if claims["iss"] != issuer:
        raise Exception("Token validation error")

    return claims


async def get_current_user(
    token: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
    user_repository: UsersRepository = Depends(get_repository(UsersRepository)),
) -> User:
    try:
        issuer = get_issuer()
        public_keys = get_cognito_public_keys()
        payload = verify_token(token.credentials, public_keys, issuer)

        if (cognito_id := payload.get("sub")) is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")

        if (user := await user_repository.get_by_cognito_id(cognito_id)) is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        return user

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")
