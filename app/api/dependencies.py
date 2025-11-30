"""Dependency injection for API routes"""
from functools import lru_cache
from app.database.connection import get_connection
from app.services.agent.graph import create_agent


@lru_cache()
def get_agent():
    """Get or create the LangGraph agent instance"""
    return create_agent()


async def get_db():
    """Get database connection from pool"""
    async with get_connection() as conn:
        yield conn

