"""Custom PostgreSQL checkpointer for LangGraph"""
import json
from uuid import uuid4, UUID
from typing import Optional, Dict, Any
from langgraph.checkpoint.base import BaseCheckpointSaver, Checkpoint, CheckpointMetadata
from app.database.connection import get_connection, execute_query, execute_command
from app.database.queries import CREATE_CHECKPOINT, GET_LATEST_CHECKPOINT
from app.core.logging import logger


class PostgresCheckpointer(BaseCheckpointSaver):
    """PostgreSQL-based checkpointer for LangGraph state"""
    
    async def put(
        self,
        config: Dict[str, Any],
        checkpoint: Checkpoint,
        metadata: CheckpointMetadata,
        new_versions: Dict[str, Any]
    ) -> None:
        """Save checkpoint to PostgreSQL"""
        try:
            thread_id = config.get("configurable", {}).get("thread_id")
            if not thread_id:
                logger.warning("No thread_id in config, skipping checkpoint save")
                return
            
            # Serialize state
            state_dict = {
                "messages": [msg.dict() if hasattr(msg, 'dict') else str(msg) for msg in checkpoint.get("messages", [])],
                "current_persona": checkpoint.get("current_persona", ""),
                "thread_id": checkpoint.get("thread_id", ""),
                "user_id": checkpoint.get("user_id", ""),
                "metadata": checkpoint.get("metadata", {})
            }
            
            checkpoint_id = uuid4()
            
            async with get_connection() as conn:
                await conn.execute(
                    CREATE_CHECKPOINT,
                    checkpoint_id,
                    UUID(thread_id) if isinstance(thread_id, str) else thread_id,
                    json.dumps(state_dict)
                )
            
            logger.debug(f"Checkpoint saved for thread {thread_id}")
        except Exception as e:
            logger.error(f"Error saving checkpoint: {str(e)}")
            raise
    
    async def get(
        self,
        config: Dict[str, Any]
    ) -> Optional[Checkpoint]:
        """Load checkpoint from PostgreSQL"""
        try:
            thread_id = config.get("configurable", {}).get("thread_id")
            if not thread_id:
                return None
            
            async with get_connection() as conn:
                row = await conn.fetchrow(
                    GET_LATEST_CHECKPOINT,
                    UUID(thread_id) if isinstance(thread_id, str) else thread_id
                )
            
            if not row:
                return None
            
            # Deserialize state
            state_dict = json.loads(row["state"])
            
            checkpoint = Checkpoint(
                messages=state_dict.get("messages", []),
                current_persona=state_dict.get("current_persona", ""),
                thread_id=state_dict.get("thread_id", ""),
                user_id=state_dict.get("user_id", ""),
                metadata=state_dict.get("metadata", {})
            )
            
            logger.debug(f"Checkpoint loaded for thread {thread_id}")
            return checkpoint
        except Exception as e:
            logger.error(f"Error loading checkpoint: {str(e)}")
            return None

