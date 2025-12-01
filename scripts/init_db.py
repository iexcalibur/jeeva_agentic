"""Initialize database schema"""
import asyncio
import os
from pathlib import Path
from app.database.connection import create_pool, close_pool
from app.database.adapter import db_adapter
from app.core.config import settings
from app.core.logging import logger


async def run_migrations():
    """Run all SQL migrations"""
    # Get migrations directory
    migrations_dir = Path(__file__).parent.parent / "app" / "database" / "migrations"
    
    # Select migration file based on database type
    if settings.DATABASE_TYPE == "sqlite":
        migration_file = migrations_dir / "001_initial_schema_sqlite.sql"
    else:
        migration_file = migrations_dir / "001_initial_schema.sql"
    
    if not migration_file.exists():
        logger.warning(f"Migration file not found: {migration_file}")
        return
    
    async with db_adapter.get_connection() as conn:
        logger.info(f"Running migration: {migration_file.name}")
        with open(migration_file, "r") as f:
            sql = f.read()
            # Execute each statement separately (SQLite doesn't support multiple statements in one execute)
            statements = [s.strip() for s in sql.split(";") if s.strip() and not s.strip().startswith("--")]
            for statement in statements:
                if statement:
                    if db_adapter.db_type == "postgresql":
                        await conn.execute(statement)
                    else:  # SQLite
                        await conn.execute(statement)
            if db_adapter.db_type == "sqlite":
                await conn.commit()
        logger.info(f"Completed migration: {migration_file.name}")


async def main():
    """Main initialization function"""
    try:
        logger.info("Initializing database...")
        await create_pool()
        await run_migrations()
        logger.info("Database initialization complete")
    except Exception as e:
        logger.error(f"Error initializing database: {str(e)}")
        raise
    finally:
        await close_pool()


if __name__ == "__main__":
    asyncio.run(main())

