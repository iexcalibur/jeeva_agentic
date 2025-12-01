"""FastAPI application entry point"""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path

from app.core.config import settings
from app.core.logging import logger
from app.core.exceptions import (
    chatbot_exception_handler,
    validation_exception_handler,
    ChatbotException
)
from fastapi.exceptions import RequestValidationError
from app.api.routes import chat, history
from app.database.connection import create_pool, close_pool
from app.database.adapter import db_adapter
from app.services.cache.adapter import cache_adapter


async def ensure_database_initialized():
    """Ensure database schema is initialized"""
    try:
        # Check if we need to initialize (for SQLite, check if tables exist)
        if settings.DATABASE_TYPE == "sqlite":
            # Check if database file exists and has tables
            db_path = Path(settings.SQLITE_DB_PATH)
            if not db_path.exists():
                logger.info("SQLite database file not found, initializing schema...")
                await initialize_database()
            else:
                # Check if users table exists
                try:
                    async with db_adapter.get_connection() as conn:
                        if db_adapter.db_type == "postgresql":
                            result = await conn.fetchval(
                                "SELECT EXISTS(SELECT 1 FROM information_schema.tables WHERE table_name = 'users')"
                            )
                        else:  # SQLite
                            cursor = await conn.execute(
                                "SELECT name FROM sqlite_master WHERE type='table' AND name='users'"
                            )
                            result = await cursor.fetchone()
                            result = result is not None  # Convert to boolean
                        if not result:
                            logger.info("Database tables not found, initializing schema...")
                            await initialize_database()
                        else:
                            logger.debug("Database schema already initialized")
                except Exception as e:
                    logger.warning(f"Error checking database schema: {e}, initializing...")
                    await initialize_database()
        else:
            # For PostgreSQL, try to initialize (will skip if already exists)
            logger.info("Ensuring PostgreSQL schema is initialized...")
            await initialize_database()
    except Exception as e:
        logger.error(f"Error ensuring database initialization: {e}")
        # Don't fail startup, but log the error
        pass


async def initialize_database():
    """Initialize database schema"""
    try:
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
            
            logger.info(f"Database schema initialized successfully")
    except Exception as e:
        logger.error(f"Error initializing database: {e}")
        raise


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup/shutdown events"""
    # Startup
    logger.info("Starting application...")
    logger.info(f"Database type: {settings.DATABASE_TYPE}, Cache type: {settings.CACHE_TYPE}")
    await create_pool()
    logger.info("Database connection pool created")
    await ensure_database_initialized()
    await cache_adapter.initialize()
    logger.info("Cache initialized")
    yield
    # Shutdown
    logger.info("Shutting down application...")
    await cache_adapter.close()
    await close_pool()
    logger.info("Database connection pool closed")


# Initialize FastAPI app
app = FastAPI(
    title="Persona Switching Chatbot",
    description="A chatbot with persona switching capabilities using LangGraph",
    version="0.1.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Exception handlers
app.add_exception_handler(ChatbotException, chatbot_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)

# Include routers
app.include_router(chat.router, prefix="/api", tags=["chat"])
app.include_router(history.router, prefix="/api", tags=["history"])


@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "Persona Switching Chatbot API", "version": "0.1.0"}


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy"}

