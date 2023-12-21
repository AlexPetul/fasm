import factory
from sqlalchemy import (
    Column,
    Integer,
    Unicode,
    create_engine,
)
from sqlalchemy.orm import (
    declarative_base,
    scoped_session,
    sessionmaker,
)
from sqlalchemy.pool import NullPool

from src.auth.models import User
from src.db.config import (
    async_session,
    get_session,
)
from src.sections.models import Section

engine = create_engine("postgresql+asyncpg://postgres:postgres@postgres:5432/postgres", echo=False, poolclass=NullPool)
session = scoped_session(sessionmaker(bind=engine))


class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = User
        sqlalchemy_session = session


class SectionFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Section
        sqlalchemy_session = session
