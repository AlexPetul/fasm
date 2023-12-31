from typing import Annotated

from fastapi import (
    APIRouter,
    Body,
    Depends,
    Request,
    status,
)

from src.auth import cognito
from src.auth.models import User
from src.auth.repository import UsersRepository
from src.auth.schemas import (
    JWTPairSchema,
    LoginSchema,
    UserSchema,
)
from src.dependencies.auth import get_current_user
from src.dependencies.database import get_repository

router = APIRouter(prefix="/auth")


@router.post(path="/login", response_model=JWTPairSchema, status_code=status.HTTP_200_OK, name="auth:login")
async def login(
    data: Annotated[LoginSchema, Body()],
    user_repository: Annotated[UsersRepository, Depends(get_repository(UsersRepository))],
):
    access, refresh = await cognito.login(data.username, data.password, user_repository=user_repository)
    return JWTPairSchema(access=access, refresh=refresh)


@router.post(path="/logout", status_code=status.HTTP_200_OK, name="auth:logout")
async def logout(request: Request):
    await cognito.logout(request.headers.get("authorization"))


@router.get(
    path="/me",
    status_code=status.HTTP_200_OK,
    response_model=UserSchema,
    name="auth:me",
)
async def me(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user
