from sqlalchemy import (
    Boolean,
    Column,
    Integer,
    String,
    func,
)
from sqlalchemy.sql import expression

from src.db.config import Base


class Verb(Base):
    __tablename__ = "verbs"

    eng = Column(String(100), primary_key=True, unique=True)
    farsi = Column(String(100))
    stem = Column(String(50))


class Vocabulary(Base):
    __tablename__ = "vocabulary"

    eng = Column(String(100), primary_key=True, unique=True)
    farsi = Column(String(100))
    preposition = Column(Boolean, server_default=expression.false(), default=False)
