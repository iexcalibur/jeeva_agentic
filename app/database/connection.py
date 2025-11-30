"""Asyncpg connection pool management"""
import asyncpg
from contextlib import asynccontextmanager
from app.core.config import settings
from app.core.logging import logger
from typing import Optional

# Global connection pool
_pool: Optional[asyncpg.Pool] = None


async def create_pool():
    """Create database connection pool"""
    global _pool
    try:
        _pool = await asyncpg.create_pool(
            settings.DATABASE_URL,
            min_size=5,
            max_size=20,
            command_timeout=60
        )
        logger.info("Database connection pool created")
    except Exception as e:
        logger.error(f"Failed to create database pool: {str(e)}")
        raise


async def close_pool():
    """Close database connection pool"""
    global _pool
    if _pool:
        await _pool.close()
        logger.info("Database connection pool closed")
        _pool = None


@asynccontextmanager
async def get_connection():
    """Get database connection from pool"""
    if not _pool:
        raise RuntimeError("Database pool not initialized. Call create_pool() first.")
    
    async with _pool.acquire() as connection:
        yield connection


async def execute_query(query: str, *args):
    """Execute a query using the connection pool"""
    async with get_connection() as conn:
        return await conn.fetch(query, *args)


async def execute_command(query: str, *args):
    """Execute a command (INSERT, UPDATE, DELETE) using the connection pool"""
    async with get_connection() as conn:
        return await conn.execute(query, *args)

