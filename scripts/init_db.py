"""Initialize database schema"""
import asyncio
import os
from pathlib import Path
from app.database.connection import create_pool, close_pool, get_connection
from app.core.logging import logger


async def run_migrations():
    """Run all SQL migrations"""
    # Get migrations directory
    migrations_dir = Path(__file__).parent.parent / "app" / "database" / "migrations"
    
    # Get all migration files sorted by name
    migration_files = sorted(migrations_dir.glob("*.sql"))
    
    if not migration_files:
        logger.warning("No migration files found")
        return
    
    async with get_connection() as conn:
        for migration_file in migration_files:
            logger.info(f"Running migration: {migration_file.name}")
            with open(migration_file, "r") as f:
                sql = f.read()
                await conn.execute(sql)
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

