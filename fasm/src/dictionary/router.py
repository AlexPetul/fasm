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
    name="dictionary:list-verbs",
    response_model=List[VerbSchema],
    dependencies=[Security(get_current_user)],
)
async def list_verbs(repository: Annotated[DictionaryRepository, Depends(get_repository(DictionaryRepository))]):
    return await repository.get_verbs()


@router.get(
    path="/vocabulary",
    status_code=status.HTTP_200_OK,
    name="verbs:list",
    response_model=List[VocabularySchema],
    dependencies=[Security(get_current_user)],
)
async def list_vocabulary(repository: Annotated[DictionaryRepository, Depends(get_repository(DictionaryRepository))]):
    return await repository.get_vocabulary()


@router.post(
    path="/vocabulary",
    status_code=status.HTTP_201_CREATED,
    name="dictionary:create-vocabulary",
    response_model=VocabularySchema,
    dependencies=[Security(get_current_user)],
)
async def create_vocabulary(
    data: Annotated[VocabularySchema, Body()],
    repository: Annotated[DictionaryRepository, Depends(get_repository(DictionaryRepository))],
):
    return await repository.create_vocabulary(**data.model_dump())


@router.post(
    path="/verbs",
    status_code=status.HTTP_200_OK,
    name="dictionary:create-verb",
    response_model=VerbSchema,
    dependencies=[Security(get_current_user)],
)
async def create_verb(
    data: Annotated[VerbSchemaCreate, Body()],
    repository: Annotated[DictionaryRepository, Depends(get_repository(DictionaryRepository))],
):
    return await repository.create_verb(**data.model_dump())
