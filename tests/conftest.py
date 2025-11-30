"""Pytest fixtures"""
import pytest
import asyncio
from app.database.connection import create_pool, close_pool
from app.core.config import settings


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def db_pool():
    """Create database connection pool for tests"""
    await create_pool()
    yield
    await close_pool()


@pytest.fixture
async def db_connection(db_pool):
    """Get database connection for tests"""
    from app.database.connection import get_connection
    async with get_connection() as conn:
        yield conn

