"""Agent nodes (persona logic)"""
from typing import Dict, Any
from langchain_core.messages import HumanMessage, AIMessage
from app.services.agent.state import AgentState
from app.services.agent.prompts import PERSONAS, DEFAULT_PERSONA
from app.services.llm.claude import create_claude_llm
from app.core.logging import logger


async def route_persona(state: AgentState) -> Dict[str, Any]:
    """Route to appropriate persona based on current_persona"""
    persona = state.get("current_persona", DEFAULT_PERSONA)
    logger.info(f"Routing to persona: {persona}")
    return {"current_persona": persona}


async def execute_persona(state: AgentState) -> Dict[str, Any]:
    """Execute persona-specific logic and generate response"""
    persona = state.get("current_persona", DEFAULT_PERSONA)
    messages = state.get("messages", [])
    
    # Get persona-specific system prompt
    system_prompt = PERSONAS.get(persona, PERSONAS[DEFAULT_PERSONA])
    
    # Create LLM with system prompt
    from langchain_core.messages import SystemMessage
    llm = create_claude_llm()
    
    # Prepare messages with system prompt
    formatted_messages = [SystemMessage(content=system_prompt)]
    for msg in messages:
        if isinstance(msg, (HumanMessage, AIMessage)):
            formatted_messages.append(msg)
        elif isinstance(msg, dict):
            # Handle dict format messages
            if msg.get("role") == "user":
                formatted_messages.append(HumanMessage(content=msg.get("content", "")))
            elif msg.get("role") == "assistant":
                formatted_messages.append(AIMessage(content=msg.get("content", "")))
    
    # Generate response
    try:
        response = await llm.ainvoke(formatted_messages)
        response_content = response.content if hasattr(response, 'content') else str(response)
        
        # Add response to messages
        new_messages = messages + [AIMessage(content=response_content)]
        
        logger.info(f"Generated response for persona {persona}")
        return {"messages": new_messages}
    except Exception as e:
        logger.error(f"Error generating response: {str(e)}")
        error_message = AIMessage(content=f"I apologize, but I encountered an error: {str(e)}")
        return {"messages": messages + [error_message]}


async def save_context(state: AgentState) -> Dict[str, Any]:
    """Save context/state (handled by checkpointer)"""
    logger.debug("Context saved via checkpointer")
    return {}

