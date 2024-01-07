from pydantic import BaseModel, EmailStr


class LoginSchema(BaseModel):
    username: str
    password: str


class SignupSchema(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: str


class JWTPairSchema(BaseModel):
    access: str


class UserSchema(BaseModel):
    id: int
    username: str
    role: str

    class Config:
        orm_mode = True
