from enum import Enum
from typing import List

from pydantic import BaseModel


class SectionSchema(BaseModel):
    id: int
    name: str
    slug: str

    class Config:
        orm_mode = True


class SectionSchemaCreate(BaseModel):
    name: str
    gpt_hint: str | None = None

    class Config:
        orm_mode = True


class QuestionType(str, Enum):
    sentence = "sentence"
    story = "story"


class QuestionSchema(BaseModel):
    id: int
    section_id: int
    content: str
    gpt_answer: str
    for_review: bool
    gpt_answer: str | None
    user_answer: str | None
    reviewer_answer: str | None

    class Config:
        orm_mode = True


class QuestionSchemaCreate(BaseModel):
    content: str | None = None
    type: QuestionType = QuestionType.sentence


class QuestionSchemaUpdate(BaseModel):
    user_answer: str | None = None
    reviewer_answer: str | None = None


class MarkForReviewSchema(BaseModel):
    ids: List[int]
