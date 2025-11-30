"""Agent state schema definition"""
from typing import TypedDict, List, Optional, Dict, Any
from langchain_core.messages import BaseMessage


class AgentState(TypedDict):
    """LangGraph agent state schema"""
    messages: List[BaseMessage]
    current_persona: str
    thread_id: str
    user_id: str
    metadata: Dict[str, Any]

