"""Thread CRUD operations"""
from uuid import uuid4, UUID
from typing import List, Optional
from datetime import datetime
from app.database.adapter import db_adapter
from app.database.queries import (
    CREATE_USER, GET_USER,
    CREATE_THREAD, GET_THREAD, GET_USER_THREADS, UPDATE_THREAD_PERSONA,
    CREATE_MESSAGE, GET_THREAD_MESSAGES
)
from app.models.database import User, Thread, Message
from app.core.logging import logger


class ThreadManager:
    """Manages thread and message operations"""
    
    async def create_user(self, user_id: str) -> User:
        """Create a new user if not exists"""
        try:
            row = await db_adapter.fetchrow(CREATE_USER, UUID(user_id))
            if row:
                return User(
                    user_id=row["user_id"],
                    created_at=row["created_at"]
                )
            # User already exists, fetch it
            row = await db_adapter.fetchrow(GET_USER, UUID(user_id))
            return User(
                user_id=row["user_id"],
                created_at=row["created_at"]
            )
        except Exception as e:
            logger.error(f"Error creating user: {str(e)}")
            raise
    
    async def create_thread(self, user_id: str, persona: str) -> Thread:
        """Create a new thread"""
        try:
            # Ensure user exists
            await self.create_user(user_id)
            
            thread_id = uuid4()
            row = await db_adapter.fetchrow(
                CREATE_THREAD,
                thread_id,
                UUID(user_id),
                persona
            )
            return Thread(
                thread_id=row["thread_id"],
                user_id=row["user_id"],
                persona=row["persona"],
                created_at=row["created_at"],
                updated_at=row["updated_at"]
            )
        except Exception as e:
            logger.error(f"Error creating thread: {str(e)}")
            raise
    
    async def get_thread(self, thread_id: str) -> Thread:
        """Get thread by ID"""
        try:
            row = await db_adapter.fetchrow(GET_THREAD, UUID(thread_id))
            if not row:
                raise ValueError(f"Thread {thread_id} not found")
            return Thread(
                thread_id=row["thread_id"],
                user_id=row["user_id"],
                persona=row["persona"],
                created_at=row["created_at"],
                updated_at=row["updated_at"]
            )
        except Exception as e:
            logger.error(f"Error getting thread: {str(e)}")
            raise
    
    async def get_user_threads(self, user_id: str) -> List[Thread]:
        """Get all threads for a user"""
        try:
            rows = await db_adapter.fetch(GET_USER_THREADS, UUID(user_id))
            return [
                Thread(
                    thread_id=row["thread_id"],
                    user_id=row["user_id"],
                    persona=row["persona"],
                    created_at=row["created_at"],
                    updated_at=row["updated_at"]
                )
                for row in rows
            ]
        except Exception as e:
            logger.error(f"Error getting user threads: {str(e)}")
            raise
    
    async def update_thread_persona(self, thread_id: str, persona: str) -> Thread:
        """Update thread persona"""
        try:
            row = await db_adapter.fetchrow(
                UPDATE_THREAD_PERSONA,
                persona,
                UUID(thread_id)
            )
            return Thread(
                thread_id=row["thread_id"],
                user_id=row["user_id"],
                persona=row["persona"],
                created_at=row["created_at"],
                updated_at=row["updated_at"]
            )
        except Exception as e:
            logger.error(f"Error updating thread persona: {str(e)}")
            raise
    
    async def save_message(self, thread_id: str, role: str, content: str) -> Message:
        """Save a message to the database"""
        try:
            message_id = uuid4()
            row = await db_adapter.fetchrow(
                CREATE_MESSAGE,
                message_id,
                UUID(thread_id),
                role,
                content
            )
            return Message(
                message_id=row["message_id"],
                thread_id=row["thread_id"],
                role=row["role"],
                content=row["content"],
                created_at=row["created_at"]
            )
        except Exception as e:
            logger.error(f"Error saving message: {str(e)}")
            raise
    
    async def get_thread_messages(self, thread_id: str) -> List[Message]:
        """Get all messages for a thread"""
        try:
            rows = await db_adapter.fetch(GET_THREAD_MESSAGES, UUID(thread_id))
            return [
                Message(
                    message_id=row["message_id"],
                    thread_id=row["thread_id"],
                    role=row["role"],
                    content=row["content"],
                    created_at=row["created_at"]
                )
                for row in rows
            ]
        except Exception as e:
            logger.error(f"Error getting thread messages: {str(e)}")
            raise

