from typing import (
    Callable,
    Type,
)

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.config import get_session
from src.db.repository import BaseRepository


def get_repository(repo_type: Type[BaseRepository]) -> Callable[[AsyncSession], BaseRepository]:
    def _get_repo(conn: AsyncSession = Depends(get_session)) -> BaseRepository:
        return repo_type(conn)

    return _get_repo
