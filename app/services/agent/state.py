"""Agent state schema definition"""
from typing import TypedDict, List, Dict, Any, Annotated
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages

class AgentState(TypedDict):
    """LangGraph agent state schema"""
    # FIX: Use Annotated[..., add_messages] to APPEND history instead of overwriting it
    messages: Annotated[List[BaseMessage], add_messages]
    
    # These fields are single values, so standard overwriting is correct
    current_persona: str
    thread_id: str
    user_id: str
    metadata: Dict[str, Any]