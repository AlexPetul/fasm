import functools
from unittest.mock import patch, Mock

import pytest
import pytest_asyncio
from fastapi import FastAPI
from httpx import (
    AsyncClient,
    Cookies,
)
from fastapi.testclient import TestClient

from src.auth.models import User
from src.dependencies.auth import get_current_user
from tests.factories import UserFactory


@pytest.fixture(scope="session", autouse=True)
def app() -> FastAPI:
    from src.main import get_application

    app = get_application()
    app.dependency_overrides[get_current_user] = lambda: UserFactory()

    return app


@pytest.fixture()
def client(app: FastAPI):
    return TestClient(
        app=app,
        base_url="http://localhost",
        headers={"Content-Type": "application/json"},
    )
