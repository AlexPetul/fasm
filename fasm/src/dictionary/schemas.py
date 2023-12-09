from pydantic import BaseModel


class VerbSchema(BaseModel):
    id: int
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
