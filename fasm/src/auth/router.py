from typing import Annotated

from fastapi import (
    APIRouter,
    Body,
    Depends,
    status, HTTPException,
)

from src.auth.models import User
from src.auth.repository import UsersRepository
from src.auth.schemas import (
    JWTPairSchema,
    LoginSchema,
    UserSchema, SignupSchema,
)
from src.auth.token import create_access_token_for_user
from src.dependencies.auth import get_current_user
from src.dependencies.database import get_repository
from src.settings import Settings, get_settings

router = APIRouter(prefix="/auth")


@router.post(path="/login", response_model=JWTPairSchema, status_code=status.HTTP_200_OK, name="auth:login")
async def login(
    data: Annotated[LoginSchema, Body()],
    user_repository: Annotated[UsersRepository, Depends(get_repository(UsersRepository))],
    settings: Settings = Depends(get_settings),
):
    user = await user_repository.get_by_username(username=data.username)
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email or password incorrect")

    if not user.check_password(data.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email or password incorrect")

    return {"access": create_access_token_for_user(user, settings)}


@router.post(path="/signup", status_code=status.HTTP_201_CREATED, name="auth:signup")
async def signup(
    data: Annotated[SignupSchema, Body()],
    user_repository: Annotated[UsersRepository, Depends(get_repository(UsersRepository))],
):
    user = await user_repository.get_by_username(username=data.username)
    if user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists")

    await user_repository.create(
        username=data.username,
        email=data.email,
        password=data.password,
        role=data.role,
    )


@router.get(
    path="/me",
    status_code=status.HTTP_200_OK,
    response_model=UserSchema,
    name="auth:me",
)
async def me(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user
