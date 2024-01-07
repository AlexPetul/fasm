import re

import bcrypt
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def generate_salt() -> str:
    return bcrypt.gensalt().decode()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def validate_password(password: str) -> bool:
    has_digit = re.findall(r"\d", password)
    has_uppercase = re.findall("[A-Z]", password)
    has_lowercase = re.findall("[a-z]", password)
    has_special_symbol = re.findall(r"[()[\]{}|\\`~!@#$%^&*_\-+=;:'\",<>./?]", password)

    return all([has_digit, has_uppercase, has_lowercase, has_special_symbol])
