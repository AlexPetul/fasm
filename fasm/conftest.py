import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from src.db.config import Base

from src.dependencies.auth import get_current_user


engine = create_engine("postgresql://postgres:postgres@postgres:5432/postgres")
session = scoped_session(sessionmaker(bind=engine))


@pytest.fixture(scope="session", autouse=True)
def app() -> FastAPI:
    from src.main import get_application
    from tests.factories import UserFactory

    app = get_application()
    app.dependency_overrides[get_current_user] = lambda: UserFactory()

    return app


@pytest.fixture
def client(app):
    reset_db()
    with TestClient(app) as client:
        yield client
    reset_db()


def reset_db():
    engine_ = engine
    session_ = session()

    with engine_.begin() as conn:
        session_.rollback()
        session.remove()

        session.close_all()
        Base.metadata.drop_all(conn)
        Base.metadata.create_all(conn)

    return engine
