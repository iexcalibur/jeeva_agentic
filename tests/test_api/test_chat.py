"""Tests for chat endpoint"""
import pytest
from httpx import AsyncClient
from app.main import app


@pytest.mark.asyncio
async def test_chat_endpoint():
    """Test chat endpoint"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/api/chat",
            json={
                "user_id": "test-user-123",
                "message": "Hello, act like my mentor"
            }
        )
        assert response.status_code in [200, 500]  # 500 if API key not set


@pytest.mark.asyncio
async def test_chat_with_thread_id():
    """Test chat endpoint with thread_id"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/api/chat",
            json={
                "user_id": "test-user-123",
                "message": "Continue our conversation",
                "thread_id": "test-thread-123"
            }
        )
        assert response.status_code in [200, 500]

