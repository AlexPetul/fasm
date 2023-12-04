from pydantic import BaseModel


class LoginSchema(BaseModel):
    username: str
    password: str


class JWTPairSchema(BaseModel):
    access: str
    refresh: str


class UserSchema(BaseModel):
    id: int
    username: str
    role: str

    class Config:
        orm_mode = True
