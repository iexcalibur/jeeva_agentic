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
        
        # For SQLite, temporarily disable foreign key checks during table creation
        if db_adapter.db_type == "sqlite":
            await conn.execute("PRAGMA foreign_keys = OFF")
        
        with open(migration_file, "r") as f:
            sql = f.read()
            # Execute each statement separately
            # Split by semicolon, but be careful with comments and multi-line statements
            statements = []
            current_statement = []
            for line in sql.split('\n'):
                line = line.strip()
                # Skip empty lines and full-line comments
                if not line or line.startswith('--'):
                    continue
                # Remove inline comments
                if '--' in line:
                    line = line[:line.index('--')].strip()
                current_statement.append(line)
                # If line ends with semicolon, it's the end of a statement
                if line.endswith(';'):
                    stmt = ' '.join(current_statement).rstrip(';').strip()
                    if stmt:
                        statements.append(stmt)
                    current_statement = []
            
            # Handle any remaining statement without trailing semicolon
            if current_statement:
                stmt = ' '.join(current_statement).strip()
                if stmt:
                    statements.append(stmt)
            
            # Execute statements one by one
            for statement in statements:
                if statement:
                    try:
                        await conn.execute(statement)
                    except Exception as e:
                        # If it's a "table already exists" error, that's okay
                        if "already exists" in str(e).lower() or "duplicate" in str(e).lower():
                            logger.debug(f"Table/Index already exists, skipping: {statement[:50]}...")
                        else:
                            logger.error(f"Error executing statement: {statement[:100]}...")
                            raise
        
        # Re-enable foreign keys for SQLite
        if db_adapter.db_type == "sqlite":
            await conn.execute("PRAGMA foreign_keys = ON")
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

