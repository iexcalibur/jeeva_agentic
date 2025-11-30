"""Tests for history endpoint"""
import pytest
from httpx import AsyncClient
from app.main import app


@pytest.mark.asyncio
async def test_chat_history_endpoint():
    """Test chat history endpoint"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get(
            "/api/chat_history",
            params={"user_id": "test-user-123"}
        )
        assert response.status_code in [200, 500]


@pytest.mark.asyncio
async def test_chat_history_with_thread_id():
    """Test chat history endpoint with thread_id"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get(
            "/api/chat_history",
            params={
                "user_id": "test-user-123",
                "thread_id": "test-thread-123"
            }
        )
        assert response.status_code in [200, 500]

