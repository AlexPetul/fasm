from sqlalchemy.ext.asyncio import AsyncSession


class BaseRepository:
    def __init__(self, conn: AsyncSession) -> None:
        self._session = conn

    @property
    def session(self) -> AsyncSession:
        return self._session
