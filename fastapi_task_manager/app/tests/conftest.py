# pylint:disable=redefined-outer-name
from unittest.mock import AsyncMock
import asgi_lifespan
import fastapi
import httpx
import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from app.main import initialize_backend_application


@pytest.fixture
def mock_async_session():
    """Фикстура мок-асинхронной сессии"""
    return AsyncMock(spec=AsyncSession)


@pytest.fixture
def sample_task_data():
    """Фикстура с примером данных задачи"""
    return {"name": "Test Task", "description": "Test Description", "status": "created"}


@pytest_asyncio.fixture(name="backend_test_app")
def backend_test_app() -> fastapi.FastAPI:
    """
    A fixture that re-initializes the FastAPI instance for test application.
    """

    return initialize_backend_application()


@pytest_asyncio.fixture(name="initialize_backend_test_application")
async def initialize_backend_test_application(
    backend_test_app: fastapi.FastAPI,
) -> fastapi.FastAPI:  # type: ignore
    async with asgi_lifespan.LifespanManager(backend_test_app):
        yield backend_test_app


@pytest_asyncio.fixture(name="async_client")
async def async_client(
    initialize_backend_test_application: fastapi.FastAPI,
) -> httpx.AsyncClient:  # type: ignore
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=initialize_backend_test_application),
        base_url="http://test",
        headers={"Content-Type": "application/json"},
    ) as client:
        yield client
