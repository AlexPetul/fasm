import os

from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
)
from sqlalchemy.orm import (
    declarative_base,
    sessionmaker,
)
from sqlalchemy.pool import NullPool

from src.settings import get_settings

POSTGRES_INDEXES_NAMING_CONVENTION = {
    "ix": "%(column_0_label)s_idx",
    "uq": "%(table_name)s_%(column_0_name)s_key",
    "ck": "%(table_name)s_%(constraint_name)s_check",
    "fk": "%(table_name)s_%(column_0_name)s_fkey",
    "pk": "%(table_name)s_pkey",
}

settings = get_settings()

Base = declarative_base(metadata=MetaData(naming_convention=POSTGRES_INDEXES_NAMING_CONVENTION))

async_engine = create_async_engine(settings.database_url, echo=False, poolclass=NullPool)
async_session = sessionmaker(async_engine, autoflush=True, expire_on_commit=False, class_=AsyncSession)


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session
