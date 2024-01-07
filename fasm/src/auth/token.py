from datetime import datetime, timedelta

import jwt
from itsdangerous import BadData, URLSafeTimedSerializer

from src.auth.models import User
from src.settings import Settings


def confirm_token(token: str, settings: Settings) -> str | None:
    serializer = URLSafeTimedSerializer(settings.secret_key.get_secret_value())
    try:
        return serializer.loads(token, salt=settings.default_salt, max_age=1800)
    except BadData:
        return None


def generate_confirmation_token(user: User, settings: Settings) -> str:
    serializer = URLSafeTimedSerializer(settings.secret_key.get_secret_value())
    return serializer.dumps(obj=user.email, salt=settings.default_salt)


def decode_jwt_token(token: str, secret_key: str):
    return jwt.decode(token, secret_key, algorithms=["HS256"])


def create_access_token_for_user(user: User, settings: Settings) -> str:
    return jwt.encode(
        payload={
            "username": user.username,
            "user_id": user.id,
            "exp": datetime.utcnow() + timedelta(minutes=settings.access_token_expires),
            "sub": "access",
        },
        algorithm="HS256",
        key=settings.access_token_secret_key.get_secret_value(),
    )
