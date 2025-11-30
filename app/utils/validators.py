"""Custom validation logic"""
from typing import Optional
from uuid import UUID


def validate_uuid(uuid_string: str) -> bool:
    """Validate UUID string format"""
    try:
        UUID(uuid_string)
        return True
    except (ValueError, TypeError):
        return False


def validate_persona(persona: str) -> bool:
    """Validate persona name"""
    from app.services.agent.prompts import PERSONAS
    return persona in PERSONAS


def sanitize_message(message: str, max_length: int = 10000) -> str:
    """Sanitize and truncate message if needed"""
    if not message:
        raise ValueError("Message cannot be empty")
    
    if len(message) > max_length:
        return message[:max_length]
    
    return message.strip()

