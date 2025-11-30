"""Custom exception handlers"""
from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from typing import Any


class ChatbotException(Exception):
    """Base exception for chatbot application"""
    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class DatabaseException(ChatbotException):
    """Database-related exceptions"""
    def __init__(self, message: str):
        super().__init__(message, status_code=500)


class LLMException(ChatbotException):
    """LLM API-related exceptions"""
    def __init__(self, message: str):
        super().__init__(message, status_code=503)


class ThreadNotFoundException(ChatbotException):
    """Thread not found exception"""
    def __init__(self, thread_id: str):
        super().__init__(f"Thread {thread_id} not found", status_code=404)


async def chatbot_exception_handler(request: Request, exc: ChatbotException) -> JSONResponse:
    """Handle custom chatbot exceptions"""
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.message, "type": exc.__class__.__name__}
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """Handle validation exceptions"""
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"error": "Validation error", "details": exc.errors()}
    )

