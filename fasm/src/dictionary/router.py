from typing import (
    Annotated,
    List,
)

from fastapi import (
    APIRouter,
    Body,
    Depends,
    Security,
    status,
)

from src.dependencies.auth import get_current_user
from src.dependencies.database import get_repository
from src.dictionary.repository import DictionaryRepository
from src.dictionary.schemas import (
    VerbSchema,
    VerbSchemaCreate,
    VocabularySchema,
)

router = APIRouter(prefix="/dictionary")


@router.get(
    path="/verbs",
    status_code=status.HTTP_200_OK,
    name="verbs:list",
    response_model=List[VerbSchema],
    dependencies=[Security(get_current_user)],
)
async def verbs(repository: Annotated[DictionaryRepository, Depends(get_repository(DictionaryRepository))]):
    return await repository.get_verbs()


@router.get(
    path="/vocabulary",
    status_code=status.HTTP_200_OK,
    name="verbs:list",
    response_model=List[VocabularySchema],
    dependencies=[Security(get_current_user)],
)
async def verbs(repository: Annotated[DictionaryRepository, Depends(get_repository(DictionaryRepository))]):
    return await repository.get_vocabulary()


@router.post(
    path="/verbs",
    status_code=status.HTTP_200_OK,
    name="verbs:create",
    response_model=VerbSchema,
    dependencies=[Security(get_current_user)],
)
async def create_verb(
    data: Annotated[VerbSchemaCreate, Body()],
    repository: Annotated[DictionaryRepository, Depends(get_repository(DictionaryRepository))],
):
    return await repository.create_verb(**data.model_dump())
