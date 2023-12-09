from sqlalchemy import select

from src.db.repository import BaseRepository
from src.dictionary.models import Verb


class DictionaryRepository(BaseRepository):
    async def get_verbs(self):
        result = await self.session.execute(select(Verb))
        return result.scalars().all()

    async def create_verb(self, **kwargs) -> Verb:
        instance = Verb(**kwargs)

        self.session.add(instance)
        await self.session.flush()
        await self.session.commit()

        return instance
