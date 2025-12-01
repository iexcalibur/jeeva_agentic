"""FastAPI application entry point"""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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
from app.services.cache.adapter import cache_adapter


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup/shutdown events"""
    # Startup
    logger.info("Starting application...")
    logger.info(f"Database type: {settings.DATABASE_TYPE}, Cache type: {settings.CACHE_TYPE}")
    await create_pool()
    logger.info("Database connection pool created")
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

