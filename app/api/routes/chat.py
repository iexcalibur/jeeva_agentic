"""Chat endpoint"""
from fastapi import APIRouter, Depends, HTTPException
from app.models.schemas import ChatRequest, ChatResponse
from app.api.dependencies import get_agent
from app.utils.persona_detector import detect_persona_switch
from app.services.memory.thread_manager import ThreadManager
from app.core.logging import logger
from datetime import datetime
from typing import Optional

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    agent = Depends(get_agent)
):
    """
    Chat endpoint that handles persona switching and message processing.
    
    1. Detect persona switch intent
    2. Route to appropriate thread (new or existing)
    3. Invoke LangGraph agent
    4. Return response
    """
    try:
        logger.info(f"Received chat request from user {request.user_id}")
        
        # Detect persona switch intent
        detected_persona = detect_persona_switch(request.message)
        logger.info(f"Detected persona: {detected_persona}")
        
        # Get or create thread
        thread_manager = ThreadManager()
        thread_id = request.thread_id
        
        if not thread_id:
            # Create new thread with detected persona
            thread = await thread_manager.create_thread(
                user_id=request.user_id,
                persona=detected_persona
            )
            thread_id = str(thread.thread_id)
        else:
            # Update thread persona if switched
            thread = await thread_manager.get_thread(thread_id)
            if thread.persona != detected_persona:
                await thread_manager.update_thread_persona(thread_id, detected_persona)
        
        # Invoke LangGraph agent
        from langchain_core.messages import HumanMessage
        config = {"configurable": {"thread_id": thread_id}}
        
        # Prepare initial state
        initial_state = {
            "messages": [HumanMessage(content=request.message)],
            "current_persona": detected_persona,
            "thread_id": thread_id,
            "user_id": request.user_id,
            "metadata": {}
        }
        
        result = await agent.ainvoke(initial_state, config=config)
        
        # Extract response from agent result
        messages = result.get("messages", [])
        if messages:
            last_message = messages[-1]
            response_text = last_message.content if hasattr(last_message, 'content') else str(last_message)
        else:
            response_text = ""
        
        # Save message to database
        await thread_manager.save_message(
            thread_id=thread_id,
            role="user",
            content=request.message
        )
        await thread_manager.save_message(
            thread_id=thread_id,
            role="assistant",
            content=response_text
        )
        
        return ChatResponse(
            thread_id=thread_id,
            persona=detected_persona,
            response=response_text,
            created_at=datetime.now()
        )
        
    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

