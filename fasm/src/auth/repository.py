from sqlalchemy import select

from src.auth.models import User
from src.db.repository import BaseRepository


class UsersRepository(BaseRepository):
    async def get_by_cognito_id(self, cognito_id: str) -> User | None:
        result = await self.session.execute(select(User).where(User.cognito_id == cognito_id))
        return result.scalars().one_or_none()

    async def create(self, cognito_id: str, email: str, username: str) -> User:
        instance = User(
            cognito_id=cognito_id,
            email=email,
            username=username,
        )

        self.session.add(instance)
        await self.session.flush()
        await self.session.commit()

        return instance
