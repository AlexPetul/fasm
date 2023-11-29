from enum import Enum

from pydantic import BaseModel


class SectionSchema(BaseModel):
    id: int
    name: str
    slug: str

    class Config:
        orm_mode = True


class SectionSchemaCreate(BaseModel):
    name: str

    class Config:
        orm_mode = True


class QuestionType(str, Enum):
    sentence = "sentence"
    story = "story"


class QuestionSchema(BaseModel):
    id: int
    content: str
    gpt_answer: str
    user_answer: str | None

    class Config:
        orm_mode = True


class QuestionSchemaCreate(BaseModel):
    type: QuestionType = QuestionType.sentence
