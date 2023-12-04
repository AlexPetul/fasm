from sqlalchemy import (
    desc,
    select,
    update,
)

from src.db.repository import BaseRepository
from src.sections.models import (
    Question,
    Section,
)


class SectionsRepository(BaseRepository):
    async def get_by_id(self, pk: int) -> Section | None:
        result = await self.session.execute(select(Section).where(Section.id == pk))
        return result.scalars().one_or_none()

    async def list(self):
        result = await self.session.execute(select(Section))
        return result.scalars().all()

    async def create(self, name: str) -> Section:
        instance = Section(name=name)

        self.session.add(instance)
        await self.session.flush()
        await self.session.commit()

        return instance


class QuestionsRepository(BaseRepository):
    async def delete(self, pk: int):
        result = await self.session.execute(select(Question).where(Question.id == pk))
        instance = result.scalars().one_or_none()

        await self.session.delete(instance)
        await self.session.commit()

    async def list(self, section_id: int, user_id: int):
        result = await self.session.execute(
            select(Question)
            .where(Question.section_id == section_id, Question.user_id == user_id)
            .order_by(desc(Question.created_at)),
        )
        return result.scalars().all()

    async def list_for_review(self):
        result = await self.session.execute(
            select(Question).where(Question.for_review == True).order_by(desc(Question.created_at))
        )
        return result.scalars().all()

    async def create(self, content: str, gpt_answer: str, section_id: int, user_id: int) -> Question:
        instance = Question(
            content=content,
            section_id=section_id,
            gpt_answer=gpt_answer,
            user_id=user_id,
        )

        self.session.add(instance)
        await self.session.flush()
        await self.session.commit()

        return instance

    async def update(self, pk: int, **kwargs):
        await self.session.execute(
            update(Question).where(Question.id == pk).values(**kwargs),
        )
        await self.session.commit()
