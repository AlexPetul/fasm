import asyncio
import os
from logging.config import fileConfig

from alembic import context
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from src.auth.models import User
from src.sections.models import Question, Section
from src.dictionary.models import Verb


config = context.config


if config.config_file_name is not None:
    fileConfig(config.config_file_name)


def run_migrations_online():
    connectable = context.config.attributes.get("connection", None)
    if connectable is None:
        connectable = create_async_engine(os.getenv("DATABASE_URL"))

    if isinstance(connectable, AsyncEngine):
        asyncio.run(run_async_migrations(connectable))
    else:
        do_run_migrations(connectable)


async def run_async_migrations(connectable):
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)
    await connectable.dispose()


def do_run_migrations(connection):
    from src.db.config import Base

    context.configure(
        connection=connection,
        target_metadata=Base.metadata,
        compare_type=True,
        render_as_batch=True,
        compare_server_default=True,
    )

    with context.begin_transaction():
        context.run_migrations()


run_migrations_online()
