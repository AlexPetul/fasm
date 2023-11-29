from sqlalchemy import (
    Column,
    Integer,
    String,
)

from src.db.config import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    cognito_id = Column(String(36), index=True)
    email = Column(String(200), unique=True, index=True)
    username = Column(String(200), unique=True, index=True)
