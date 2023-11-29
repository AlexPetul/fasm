import os

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

Base = declarative_base()

async_engine = create_async_engine(os.getenv("DATABASE_URL"), echo=False, poolclass=NullPool)
async_session = sessionmaker(async_engine, autoflush=True, expire_on_commit=False, class_=AsyncSession)


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session
