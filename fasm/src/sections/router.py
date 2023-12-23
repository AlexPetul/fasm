from typing import (
    Annotated,
    List,
)

from fastapi import (
    Body,
    Depends,
    Security,
    status,
)
from fastapi_restful.cbv import cbv
from fastapi_restful.inferring_router import InferringRouter

from src.auth.models import User
from src.dependencies.auth import get_current_user
from src.dependencies.database import get_repository
from src.sections import gpt
from src.sections.repository import (
    QuestionsRepository,
    SectionsRepository,
)
from src.sections.schemas import (
    QuestionSchema,
    QuestionSchemaCreate,
    QuestionSchemaUpdate,
    SectionRuleSchema,
    SectionSchema,
)

router = InferringRouter()


@cbv(router)
class SectionsView:
    user: User = Security(get_current_user)
    repository: SectionsRepository = Depends(get_repository(SectionsRepository))

    @router.get("/sections", name="sections:list")
    async def list_sections(self) -> List[SectionSchema]:
        """Get list of available sections."""
        return await self.repository.list()

    @router.get("/sections/{pk}/rules", name="sections:list-rules")
    async def list_rules(self, pk: Annotated[int, "Section's primary key"]) -> SectionRuleSchema:
        """Get rules for certain section, including grammar and examples."""
        return await self.repository.get_rule(pk)


@cbv(router)
class QuestionsView:
    user: User = Security(get_current_user)
    questions_repository: QuestionsRepository = Depends(get_repository(QuestionsRepository))
    sections_repository: SectionsRepository = Depends(get_repository(SectionsRepository))

    @router.post("/sections/{pk}/questions", name="questions:list-create", status_code=status.HTTP_201_CREATED)
    async def create_question(
        self,
        pk: Annotated[int, "Section's primary key"],
        data: Annotated[QuestionSchemaCreate, Body()],
    ) -> QuestionSchema:
        section = await self.sections_repository.get_by_id(pk)

        if data.content is not None:
            return await self.questions_repository.create(
                content=data.content,
                section_id=pk,
                user_id=self.user.id,
            )

        question_n_answer = await gpt.ask(
            section=section.name,
            question_type=data.type,
            hint=section.gpt_hint,
        )

        return await self.questions_repository.create(
            content=question_n_answer["question"],
            gpt_answer=question_n_answer["answer"],
            section_id=pk,
            user_id=self.user.id,
        )

    @router.get("/sections/{pk}/questions", name="questions:list")
    async def list_questions(self, pk: Annotated[int, "Section's primary key'"]) -> List[QuestionSchema]:
        return await self.questions_repository.list(
            section_id=pk,
            user_id=self.user.id,
        )

    @router.delete(
        "/sections/{section_id}/questions/{pk}",
        name="questions:delete",
        status_code=status.HTTP_204_NO_CONTENT,
    )
    async def delete_question(self, pk: Annotated[int, "Question's primary key"]) -> None:
        await self.questions_repository.delete(pk)

    @router.patch("/sections/{section_id}/questions/{pk}", name="questions:update")
    async def update_question(
        self,
        pk: Annotated[int, "Question's primary key"],
        data: Annotated[QuestionSchemaUpdate, Body()],
    ):
        await self.questions_repository.update(pk, **data.model_dump(exclude_none=True))
