from sqlalchemy import select

from src.auth.models import User
from src.db.repository import BaseRepository


class UsersRepository(BaseRepository):
    async def get_by_username(self, username: str) -> User | None:
        result = await self.session.execute(select(User).where(User.username == username))
        return result.scalars().one_or_none()

    async def create(self, email: str, username: str, role: str, password: str) -> User:
        instance = User(
            email=email,
            username=username,
            role=role,
        )
        instance.change_password(password)

        self.session.add(instance)
        await self.session.flush()
        await self.session.commit()

        return instance
