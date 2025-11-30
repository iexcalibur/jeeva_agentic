"""LangGraph state graph definition"""
from langgraph.graph import StateGraph, END
from app.services.agent.state import AgentState
from app.services.agent.nodes import route_persona, execute_persona, save_context
from app.services.memory.checkpointer import PostgresCheckpointer
from app.core.logging import logger


def create_agent():
    """Create and compile LangGraph agent with PostgreSQL checkpointer"""
    try:
        # Create checkpointer
        checkpointer = PostgresCheckpointer()
        
        # Create state graph
        workflow = StateGraph(AgentState)
        
        # Add nodes
        workflow.add_node("route_persona", route_persona)
        workflow.add_node("execute_persona", execute_persona)
        workflow.add_node("save_context", save_context)
        
        # Set entry point
        workflow.set_entry_point("route_persona")
        
        # Add edges
        workflow.add_edge("route_persona", "execute_persona")
        workflow.add_edge("execute_persona", "save_context")
        workflow.add_edge("save_context", END)
        
        # Compile graph with checkpointer
        # Note: LangGraph checkpointer interface may vary by version
        try:
            app = workflow.compile(checkpointer=checkpointer)
        except TypeError:
            # Fallback if checkpointer interface is different
            logger.warning("Using graph without checkpointer (checkpointer interface may differ)")
            app = workflow.compile()
        
        logger.info("LangGraph agent created and compiled successfully")
        return app
    except Exception as e:
        logger.error(f"Failed to create agent: {str(e)}")
        raise

