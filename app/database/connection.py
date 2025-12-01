"""Database connection management using adapter"""
from contextlib import asynccontextmanager
from app.database.adapter import db_adapter
from app.core.logging import logger

# Re-export adapter functions for backward compatibility
async def create_pool():
    """Create database connection pool"""
    await db_adapter.create_pool()


async def close_pool():
    """Close database connection pool"""
    await db_adapter.close_pool()


@asynccontextmanager
async def get_connection():
    """Get database connection"""
    async with db_adapter.get_connection() as conn:
        yield conn


async def execute_query(query: str, *args):
    """Execute a query using the connection pool"""
    return await db_adapter.execute_query(query, *args)


async def execute_command(query: str, *args):
    """Execute a command (INSERT, UPDATE, DELETE) using the connection pool"""
    return await db_adapter.execute_command(query, *args)

