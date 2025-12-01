"""Thread CRUD operations"""
from uuid import uuid4, UUID, uuid5, NAMESPACE_DNS
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
from app.core.config import settings


def _to_uuid(value):
    """Convert value to UUID, handling both string and UUID types"""
    if value is None:
        raise ValueError("Cannot convert None to UUID")
    if isinstance(value, UUID):
        return value
    if isinstance(value, str):
        # Strip whitespace and handle empty strings
        value = value.strip()
        if not value:
            raise ValueError("Cannot convert empty string to UUID")
        try:
            # Try to parse as UUID first
            return UUID(value)
        except (ValueError, AttributeError):
            # If it's not a valid UUID string, generate a deterministic UUID from it
            # Using UUID5 (name-based) to ensure same string always generates same UUID
            return uuid5(NAMESPACE_DNS, value)
    # For other types, try to convert to string first
    try:
        str_value = str(value)
        try:
            return UUID(str_value)
        except ValueError:
            # Generate deterministic UUID from string representation
            return uuid5(NAMESPACE_DNS, str_value)
    except (ValueError, AttributeError) as e:
        logger.error(f"Cannot convert {type(value)} to UUID: {value!r}")
        raise ValueError(f"Cannot convert {type(value).__name__} to UUID: {value}") from e


def _normalize_user_id(user_id: str) -> UUID:
    """Normalize user_id to UUID format (handles non-UUID strings)"""
    return _to_uuid(user_id)


class ThreadManager:
    """Manages thread and message operations"""
    
    async def create_user(self, user_id: str) -> User:
        """Create a new user if not exists"""
        try:
            # Normalize user_id to UUID (handles non-UUID strings like "user_123")
            normalized_user_id = _normalize_user_id(user_id)
            
            # Try to get user first (check if exists)
            row = await db_adapter.fetchrow(GET_USER, normalized_user_id)
            if row:
                # User already exists, return it
                return User(
                    user_id=_to_uuid(row["user_id"]),
                    created_at=row["created_at"]
                )
            
            # User doesn't exist, create it
            # Note: For SQLite, ON CONFLICT DO NOTHING with RETURNING returns no rows on conflict
            # So we try to insert, and if it returns None, we fetch the user
            row = await db_adapter.fetchrow(CREATE_USER, normalized_user_id)
            
            if row:
                # User was created successfully
                return User(
                    user_id=_to_uuid(row["user_id"]),
                    created_at=row["created_at"]
                )
            
            # INSERT returned None (ON CONFLICT DO NOTHING in SQLite doesn't return rows)
            # This means user was created but RETURNING didn't work, or there was a race condition
            # Fetch the user to verify it exists
            row = await db_adapter.fetchrow(GET_USER, normalized_user_id)
            if not row:
                raise ValueError(f"Failed to create user: {user_id} (user not found after creation attempt)")
            
            return User(
                user_id=_to_uuid(row["user_id"]),
                created_at=row["created_at"]
            )
        except Exception as e:
            logger.error(f"Error creating user: {str(e)}")
            raise
    
    async def create_thread(self, user_id: str, persona: str) -> Thread:
        """Create a new thread"""
        try:
            # Ensure user exists first (this will create it if needed)
            user = await self.create_user(user_id)
            
            # Use the normalized user_id from the created user object to ensure consistency
            normalized_user_id = user.user_id  # This is already a UUID object
            
            logger.debug(f"Creating thread for user_id: {normalized_user_id}, persona: {persona}")
            
            thread_id = uuid4()
            row = await db_adapter.fetchrow(
                CREATE_THREAD,
                thread_id,
                normalized_user_id,  # Use UUID object directly
                persona
            )
            
            if not row:
                raise ValueError(f"Failed to create thread: no row returned")
            
            return Thread(
                thread_id=_to_uuid(row["thread_id"]),
                user_id=_to_uuid(row["user_id"]),
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
                thread_id=_to_uuid(row["thread_id"]),
                user_id=_to_uuid(row["user_id"]),
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
            # Normalize user_id to UUID
            normalized_user_id = _normalize_user_id(user_id)
            rows = await db_adapter.fetch(GET_USER_THREADS, normalized_user_id)
            return [
                Thread(
                    thread_id=_to_uuid(row["thread_id"]),
                    user_id=_to_uuid(row["user_id"]),
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
                thread_id=_to_uuid(row["thread_id"]),
                user_id=_to_uuid(row["user_id"]),
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
                message_id=_to_uuid(row["message_id"]),
                thread_id=_to_uuid(row["thread_id"]),
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
                    message_id=_to_uuid(row["message_id"]),
                    thread_id=_to_uuid(row["thread_id"]),
                    role=row["role"],
                    content=row["content"],
                    created_at=row["created_at"]
                )
                for row in rows
            ]
        except Exception as e:
            logger.error(f"Error getting thread messages: {str(e)}")
            raise

