"""Tests for thread manager"""
import pytest
from app.services.memory.thread_manager import ThreadManager


@pytest.mark.asyncio
async def test_create_thread(db_connection):
    """Test thread creation"""
    manager = ThreadManager()
    thread = await manager.create_thread(
        user_id="test-user-123",
        persona="mentor"
    )
    assert thread is not None
    assert thread.persona == "mentor"


@pytest.mark.asyncio
async def test_get_thread(db_connection):
    """Test getting a thread"""
    manager = ThreadManager()
    thread = await manager.create_thread(
        user_id="test-user-123",
        persona="investor"
    )
    retrieved = await manager.get_thread(str(thread.thread_id))
    assert retrieved.thread_id == thread.thread_id
    assert retrieved.persona == "investor"

