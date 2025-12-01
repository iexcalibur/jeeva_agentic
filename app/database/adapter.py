"""Database adapter supporting both SQLite and PostgreSQL"""
import aiosqlite
import asyncpg
import re
from uuid import UUID
from typing import Union, Optional, Any, Dict
from contextlib import asynccontextmanager
from app.core.config import settings
from app.core.logging import logger


class DatabaseAdapter:
    """Adapter for database operations supporting SQLite and PostgreSQL"""
    
    def __init__(self):
        self._pool: Optional[Union[asyncpg.Pool, Any]] = None
        self.db_type = settings.DATABASE_TYPE
    
    async def create_pool(self):
        """Create database connection pool"""
        if self.db_type == "postgresql":
            try:
                # Extract connection string from DATABASE_URL
                db_url = settings.DATABASE_URL.replace("postgresql://", "").replace("postgresql+asyncpg://", "")
                parts = db_url.split("@")
                if len(parts) == 2:
                    auth, host_db = parts
                    user, password = auth.split(":")
                    host, port_db = host_db.split("/")
                    host, port = host.split(":")
                    db_name = port_db
                else:
                    # Fallback to individual settings
                    user = settings.POSTGRES_USER
                    password = settings.POSTGRES_PASSWORD
                    host = settings.POSTGRES_HOST
                    port = settings.POSTGRES_PORT
                    db_name = settings.POSTGRES_DB
                
                self._pool = await asyncpg.create_pool(
                    host=host,
                    port=int(port),
                    user=user,
                    password=password,
                    database=db_name,
                    min_size=5,
                    max_size=20,
                    command_timeout=60
                )
                logger.info("PostgreSQL connection pool created")
            except Exception as e:
                logger.error(f"Failed to create PostgreSQL pool: {str(e)}")
                raise
        else:  # SQLite
            # SQLite doesn't use a pool, but we'll create the connection file
            db_path = settings.SQLITE_DB_PATH
            # Ensure directory exists
            import os
            os.makedirs(os.path.dirname(db_path) if os.path.dirname(db_path) else ".", exist_ok=True)
            # Test connection
            async with aiosqlite.connect(db_path) as conn:
                await conn.execute("SELECT 1")
            logger.info(f"SQLite database initialized at {db_path}")
    
    async def close_pool(self):
        """Close database connection pool"""
        if self.db_type == "postgresql" and self._pool:
            await self._pool.close()
            logger.info("PostgreSQL connection pool closed")
        self._pool = None
    
    @asynccontextmanager
    async def get_connection(self):
        """Get database connection"""
        if self.db_type == "postgresql":
            if not self._pool:
                raise RuntimeError("Database pool not initialized. Call create_pool() first.")
            async with self._pool.acquire() as connection:
                yield connection
        else:  # SQLite
            async with aiosqlite.connect(settings.SQLITE_DB_PATH) as connection:
                # Enable foreign keys for SQLite
                await connection.execute("PRAGMA foreign_keys = ON")
                yield connection
    
    def _convert_query_for_sqlite(self, query: str) -> str:
        """Convert PostgreSQL query to SQLite-compatible query"""
        sqlite_query = query
        
        # Convert PostgreSQL functions to SQLite equivalents
        sqlite_query = sqlite_query.replace("NOW()", "CURRENT_TIMESTAMP")
        sqlite_query = sqlite_query.replace("::jsonb", "")  # SQLite doesn't have jsonb type, just TEXT
        
        # Convert parameter placeholders ($1, $2, etc. to ?)
        # Find all parameter placeholders and replace them in reverse order to avoid conflicts
        param_matches = list(re.finditer(r'\$(\d+)', sqlite_query))
        if param_matches:
            # Replace in reverse order to maintain positions
            for match in reversed(param_matches):
                param_num = match.group(1)
                sqlite_query = sqlite_query[:match.start()] + "?" + sqlite_query[match.end():]
        
        return sqlite_query
    
    async def execute_query(self, query: str, *args):
        """Execute a SELECT query"""
        async with self.get_connection() as conn:
            if self.db_type == "postgresql":
                return await conn.fetch(query, *args)
            else:  # SQLite
                # Convert PostgreSQL query to SQLite
                sqlite_query = self._convert_query_for_sqlite(query)
                # Convert UUID objects to strings for SQLite
                sqlite_args = [str(arg) if isinstance(arg, UUID) else arg for arg in args]
                cursor = await conn.execute(sqlite_query, sqlite_args)
                rows = await cursor.fetchall()
                # Convert to list of dict-like objects
                columns = [desc[0] for desc in cursor.description] if cursor.description else []
                return [dict(zip(columns, row)) for row in rows]
    
    async def execute_command(self, query: str, *args):
        """Execute an INSERT/UPDATE/DELETE command"""
        async with self.get_connection() as conn:
            if self.db_type == "postgresql":
                return await conn.execute(query, *args)
            else:  # SQLite
                # Convert PostgreSQL query to SQLite
                sqlite_query = self._convert_query_for_sqlite(query)
                # Convert UUID objects to strings for SQLite
                sqlite_args = [str(arg) if isinstance(arg, UUID) else arg for arg in args]
                cursor = await conn.execute(sqlite_query, sqlite_args)
                await conn.commit()
                # Return rowcount for compatibility
                return cursor.rowcount if hasattr(cursor, 'rowcount') else 0
    
    async def fetchrow(self, query: str, *args):
        """Fetch a single row"""
        async with self.get_connection() as conn:
            if self.db_type == "postgresql":
                return await conn.fetchrow(query, *args)
            else:  # SQLite
                # Convert PostgreSQL query to SQLite
                sqlite_query = self._convert_query_for_sqlite(query)
                # Convert UUID objects to strings for SQLite
                sqlite_args = [str(arg) if isinstance(arg, UUID) else arg for arg in args]
                cursor = await conn.execute(sqlite_query, sqlite_args)
                # Check if this is a modification query (INSERT/UPDATE/DELETE) and commit if so
                query_upper = sqlite_query.strip().upper()
                if any(query_upper.startswith(cmd) for cmd in ('INSERT', 'UPDATE', 'DELETE')):
                    await conn.commit()
                row = await cursor.fetchone()
                if not row:
                    return None
                columns = [desc[0] for desc in cursor.description] if cursor.description else []
                return dict(zip(columns, row))
    
    async def fetch(self, query: str, *args):
        """Fetch multiple rows"""
        return await self.execute_query(query, *args)


# Global adapter instance
db_adapter = DatabaseAdapter()

