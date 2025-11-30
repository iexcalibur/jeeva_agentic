"""Pydantic request/response models"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class ChatRequest(BaseModel):
    """Chat request model"""
    user_id: str = Field(..., description="User identifier")
    message: str = Field(..., description="User message")
    thread_id: Optional[str] = Field(None, description="Optional thread identifier")


class ChatResponse(BaseModel):
    """Chat response model"""
    thread_id: str = Field(..., description="Thread identifier")
    persona: str = Field(..., description="Current persona")
    response: str = Field(..., description="Assistant response")
    created_at: datetime = Field(..., description="Response timestamp")


class Message(BaseModel):
    """Message model"""
    role: str = Field(..., description="Message role (user or assistant)")
    content: str = Field(..., description="Message content")
    created_at: datetime = Field(..., description="Message timestamp")


class Thread(BaseModel):
    """Thread model"""
    thread_id: str = Field(..., description="Thread identifier")
    user_id: str = Field(..., description="User identifier")
    persona: str = Field(..., description="Thread persona")
    created_at: datetime = Field(..., description="Thread creation timestamp")
    updated_at: datetime = Field(..., description="Thread update timestamp")


class ChatHistoryResponse(BaseModel):
    """Chat history response model"""
    threads: List[Thread] = Field(..., description="List of threads")
    messages: List[Message] = Field(default_factory=list, description="Messages for specific thread")


class ErrorResponse(BaseModel):
    """Error response model"""
    error: str = Field(..., description="Error message")
    type: Optional[str] = Field(None, description="Error type")
    details: Optional[dict] = Field(None, description="Error details")

