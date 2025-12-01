"""Chat endpoint"""
from fastapi import APIRouter, Depends, HTTPException
from app.models.schemas import ChatRequest, ChatResponse
from app.api.dependencies import get_agent
from app.utils.persona_detector import detect_persona_switch
from app.services.memory.thread_manager import ThreadManager
from app.services.agent.prompts import DEFAULT_PERSONA
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
    
    1. Detect persona switch intent (returns None if no switch requested)
    2. Route to appropriate thread:
       - If switch detected: find existing thread for that persona or create new one
       - If no switch: continue in current thread (or create default if none exists)
    3. Invoke LangGraph agent
    4. Return response
    """
    try:
        logger.info(f"Received chat request from user {request.user_id}, thread_id: {request.thread_id}")
        
        thread_manager = ThreadManager()
        target_persona: Optional[str] = None
        final_thread_id: Optional[str] = None
        current_thread = None
        
        # Get current thread if thread_id provided
        if request.thread_id:
            try:
                current_thread = await thread_manager.get_thread(request.thread_id)
                logger.info(f"Current thread persona: {current_thread.persona}")
            except (ValueError, Exception) as e:
                logger.warning(f"Thread {request.thread_id} not found or invalid: {str(e)}")
                current_thread = None
        
        # Detect persona switch intent
        detected_persona_switch = detect_persona_switch(request.message)
        logger.info(f"Detected persona switch: {detected_persona_switch}")
        
        # Handle persona switching logic
        if detected_persona_switch:
            # A specific persona switch was requested
            target_persona = detected_persona_switch
            
            # Check if we're already in a thread with this persona
            if current_thread and current_thread.persona == target_persona:
                # Already in the correct thread, continue using it
                final_thread_id = str(current_thread.thread_id)
                logger.info(f"Already in {target_persona} thread, continuing")
            else:
                # Need to switch - check if user already has an existing thread for this persona
                existing_threads = await thread_manager.get_user_threads(request.user_id)
                target_thread = next(
                    (t for t in existing_threads if t.persona == target_persona),
                    None
                )
                
                if target_thread:
                    # Switch to existing thread (long-term memory recall)
                    final_thread_id = str(target_thread.thread_id)
                    logger.info(f"Switching to existing {target_persona} thread: {final_thread_id}")
                else:
                    # Create NEW thread for this persona
                    new_thread = await thread_manager.create_thread(
                        user_id=request.user_id,
                        persona=target_persona
                    )
                    final_thread_id = str(new_thread.thread_id)
                    logger.info(f"Created new {target_persona} thread: {final_thread_id}")
        else:
            # No persona switch requested - continue in current context
            if current_thread:
                # Continue in existing thread
                final_thread_id = str(current_thread.thread_id)
                target_persona = current_thread.persona
                logger.info(f"Continuing in existing {target_persona} thread: {final_thread_id}")
            else:
                # First time user, no thread, no specific persona -> Default
                target_persona = DEFAULT_PERSONA
                new_thread = await thread_manager.create_thread(
                    user_id=request.user_id,
                    persona=target_persona
                )
                final_thread_id = str(new_thread.thread_id)
                logger.info(f"Created default {target_persona} thread for new user: {final_thread_id}")
        
        # Ensure we have a valid thread_id at this point
        if not final_thread_id:
            raise ValueError("Failed to determine thread_id")
        
        # Get the final thread to ensure it exists
        final_thread = await thread_manager.get_thread(final_thread_id)
        target_persona = final_thread.persona  # Use the thread's actual persona
        
        # Invoke LangGraph agent
        from langchain_core.messages import HumanMessage
        config = {"configurable": {"thread_id": final_thread_id}}
        
        # Prepare initial state
        initial_state = {
            "messages": [HumanMessage(content=request.message)],
            "current_persona": target_persona,
            "thread_id": final_thread_id,
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
            thread_id=final_thread_id,
            role="user",
            content=request.message
        )
        await thread_manager.save_message(
            thread_id=final_thread_id,
            role="assistant",
            content=response_text
        )
        
        return ChatResponse(
            thread_id=final_thread_id,
            persona=target_persona,
            response=response_text,
            created_at=datetime.now()
        )
        
    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

