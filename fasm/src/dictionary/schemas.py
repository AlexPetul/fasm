from pydantic import BaseModel


class VerbSchema(BaseModel):
    eng: str
    farsi: str
    stem: str

    class Config:
        orm_mode = True


class VerbSchemaCreate(BaseModel):
    eng: str
    farsi: str
    stem: str

    class Config:
        orm_mode = True


class VocabularySchema(BaseModel):
    eng: str
    farsi: str
    preposition: bool = False

    class Config:
        orm_mode = True
