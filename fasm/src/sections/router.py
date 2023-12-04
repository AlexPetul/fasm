from typing import (
    Annotated,
    List,
)

from fastapi import (
    APIRouter,
    BackgroundTasks,
    Body,
    Depends,
    Security,
    status,
)

from src.auth.models import User
from src.dependencies.auth import get_current_user
from src.dependencies.database import get_repository
from src.sections import (
    gpt,
    notifications,
)
from src.sections.repository import (
    QuestionsRepository,
    SectionsRepository,
)
from src.sections.schemas import (
    MarkForReviewSchema,
    QuestionSchema,
    QuestionSchemaCreate,
    QuestionSchemaUpdate,
    SectionSchema,
    SectionSchemaCreate,
)

router = APIRouter(prefix="/sections")


@router.get(
    path="",
    status_code=status.HTTP_200_OK,
    name="sections:list",
    response_model=List[SectionSchema],
    dependencies=[Security(get_current_user)],
)
async def sections(repository: Annotated[SectionsRepository, Depends(get_repository(SectionsRepository))]):
    return await repository.list()


@router.post(
    path="",
    status_code=status.HTTP_201_CREATED,
    name="sections:create",
    response_model=SectionSchema,
    dependencies=[Security(get_current_user)],
)
async def create_section(
    data: Annotated[SectionSchemaCreate, Body()],
    repository: Annotated[SectionsRepository, Depends(get_repository(SectionsRepository))],
):
    return await repository.create(name=data.name)


@router.post(
    path="/{pk}/questions",
    status_code=status.HTTP_201_CREATED,
    name="questions:create",
    response_model=QuestionSchema,
)
async def create_question(
    pk: Annotated[int, "Section's primary key"],
    data: Annotated[QuestionSchemaCreate, Body()],
    current_user: Annotated[User, Depends(get_current_user)],
    questions_repository: Annotated[QuestionsRepository, Depends(get_repository(QuestionsRepository))],
    sections_repository: Annotated[SectionsRepository, Depends(get_repository(SectionsRepository))],
):
    section = await sections_repository.get_by_id(pk)

    question_n_answer = await gpt.ask(section=section.name, question_type=data.type)

    return await questions_repository.create(
        content=question_n_answer["question"],
        gpt_answer=question_n_answer["answer"],
        section_id=pk,
        user_id=current_user.id,
    )


@router.get(
    path="/{pk}/questions",
    name="questions:list",
    response_model=List[QuestionSchema],
)
async def list_questions(
    pk: Annotated[int, "Section's primary key'"],
    current_user: Annotated[User, Depends(get_current_user)],
    repository: Annotated[QuestionsRepository, Depends(get_repository(QuestionsRepository))],
):
    return await repository.list(
        section_id=pk,
        user_id=current_user.id,
    )


@router.delete(
    path="/{section_id}/questions/{pk}",
    name="questions:delete",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Security(get_current_user)],
)
async def list_questions(
    pk: Annotated[int, "Question's primary key"],
    repository: Annotated[QuestionsRepository, Depends(get_repository(QuestionsRepository))],
):
    await repository.delete(pk)


@router.patch(
    path="/{section_id}/questions/{pk}",
    name="questions:patch",
    dependencies=[Security(get_current_user)],
)
async def update_question(
    pk: Annotated[int, "Question's primary key"],
    data: Annotated[QuestionSchemaUpdate, Body()],
    repository: Annotated[QuestionsRepository, Depends(get_repository(QuestionsRepository))],
):
    await repository.update(pk, **data.model_dump(exclude_none=True))


@router.patch(
    path="/{section_id}/questions",
    name="questions:mark_for_review",
)
async def mark_for_review(
    data: Annotated[MarkForReviewSchema, Body()],
    current_user: Annotated[User, Depends(get_current_user)],
    repository: Annotated[QuestionsRepository, Depends(get_repository(QuestionsRepository))],
    worker: Annotated[BackgroundTasks, "Worker to send notifications"],
):
    for pk in data.ids:
        await repository.update(pk, for_review=True)

    worker.add_task(
        notifications.send_sms,
        username=current_user.username,
        questions_count=len(data.ids),
    )


@router.get(
    path="/questions",
    name="questions:list-all",
    response_model=List[QuestionSchema],
)
async def get_all(
    repository: Annotated[QuestionsRepository, Depends(get_repository(QuestionsRepository))],
):
    return await repository.list_for_review()
