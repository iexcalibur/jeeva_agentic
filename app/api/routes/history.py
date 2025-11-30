"""Chat history endpoint"""
from fastapi import APIRouter, Query, HTTPException
from app.models.schemas import ChatHistoryResponse, Thread, Message
from app.services.memory.thread_manager import ThreadManager
from app.core.logging import logger
from typing import Optional

router = APIRouter()


@router.get("/chat_history", response_model=ChatHistoryResponse)
async def get_chat_history(
    user_id: str = Query(..., description="User identifier"),
    thread_id: Optional[str] = Query(None, description="Optional thread identifier")
):
    """
    Get chat history for a user.
    
    If thread_id is provided, returns messages for that thread.
    Otherwise, returns all threads for the user.
    """
    try:
        logger.info(f"Fetching chat history for user {user_id}, thread {thread_id}")
        
        thread_manager = ThreadManager()
        
        if thread_id:
            # Get messages for specific thread
            messages = await thread_manager.get_thread_messages(thread_id)
            thread = await thread_manager.get_thread(thread_id)
            
            return ChatHistoryResponse(
                threads=[Thread(
                    thread_id=str(thread.thread_id),
                    user_id=str(thread.user_id),
                    persona=thread.persona,
                    created_at=thread.created_at,
                    updated_at=thread.updated_at
                )],
                messages=[
                    Message(
                        role=msg.role,
                        content=msg.content,
                        created_at=msg.created_at
                    )
                    for msg in messages
                ]
            )
        else:
            # Get all threads for user
            threads = await thread_manager.get_user_threads(user_id)
            
            return ChatHistoryResponse(
                threads=[
                    Thread(
                        thread_id=str(t.thread_id),
                        user_id=str(t.user_id),
                        persona=t.persona,
                        created_at=t.created_at,
                        updated_at=t.updated_at
                    )
                    for t in threads
                ],
                messages=[]
            )
            
    except Exception as e:
        logger.error(f"Error in chat_history endpoint: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

