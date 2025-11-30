"""Database table definitions (SQLAlchemy-style, but using asyncpg)"""
from typing import Optional
from datetime import datetime
from uuid import UUID


class User:
    """User model"""
    def __init__(
        self,
        user_id: UUID,
        created_at: datetime
    ):
        self.user_id = user_id
        self.created_at = created_at


class Thread:
    """Thread model"""
    def __init__(
        self,
        thread_id: UUID,
        user_id: UUID,
        persona: str,
        created_at: datetime,
        updated_at: datetime
    ):
        self.thread_id = thread_id
        self.user_id = user_id
        self.persona = persona
        self.created_at = created_at
        self.updated_at = updated_at


class Message:
    """Message model"""
    def __init__(
        self,
        message_id: UUID,
        thread_id: UUID,
        role: str,
        content: str,
        created_at: datetime
    ):
        self.message_id = message_id
        self.thread_id = thread_id
        self.role = role
        self.content = content
        self.created_at = created_at


class Checkpoint:
    """Checkpoint model for LangGraph state"""
    def __init__(
        self,
        checkpoint_id: UUID,
        thread_id: UUID,
        state: dict,
        created_at: datetime
    ):
        self.checkpoint_id = checkpoint_id
        self.thread_id = thread_id
        self.state = state
        self.created_at = created_at

