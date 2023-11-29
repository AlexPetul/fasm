from pydantic import BaseModel


class LoginSchema(BaseModel):
    username: str
    password: str


class JWTPairSchema(BaseModel):
    access: str
    refresh: str
