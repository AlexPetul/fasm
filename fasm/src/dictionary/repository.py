from sqlalchemy import select

from src.db.repository import BaseRepository
from src.dictionary.models import (
    Verb,
    Vocabulary,
)


class DictionaryRepository(BaseRepository):
    async def get_verbs(self):
        result = await self.session.execute(select(Verb))
        return result.scalars().all()

    async def get_vocabulary(self):
        result = await self.session.execute(select(Vocabulary).order_by(Vocabulary.eng))
        return result.scalars().all()

    async def create_vocabulary(self, **kwargs) -> Verb:
        instance = Vocabulary(**kwargs)

        self.session.add(instance)
        await self.session.flush()
        await self.session.commit()

        return instance

    async def create_verb(self, **kwargs) -> Verb:
        instance = Verb(**kwargs)

        self.session.add(instance)
        await self.session.flush()
        await self.session.commit()

        return instance
