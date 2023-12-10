from sqlalchemy import (
    Column,
    Integer,
    String,
)

from src.db.config import Base


class Verb(Base):
    __tablename__ = "verbs"

    id = Column(Integer, primary_key=True, index=True)
    eng = Column(String(100), unique=True)
    farsi = Column(String(100))
    stem = Column(String(50))


class Vocabulary(Base):
    __tablename__ = "vocabulary"

    eng = Column(String(100), primary_key=True, unique=True)
    farsi = Column(String(100))
