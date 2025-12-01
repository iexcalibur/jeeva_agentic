"""Custom database checkpointer for LangGraph (supports SQLite and PostgreSQL)"""
import json
from uuid import uuid4, UUID
from typing import Optional, Dict, Any
from langgraph.checkpoint.base import BaseCheckpointSaver, Checkpoint, CheckpointMetadata
from app.database.adapter import db_adapter
from app.database.queries import CREATE_CHECKPOINT, GET_LATEST_CHECKPOINT
from app.core.logging import logger


class DatabaseCheckpointer(BaseCheckpointSaver):
    """Database-based checkpointer for LangGraph state (supports SQLite and PostgreSQL)"""
    
    async def put(
        self,
        config: Dict[str, Any],
        checkpoint: Checkpoint,
        metadata: CheckpointMetadata,
        new_versions: Dict[str, Any]
    ) -> None:
        """Save checkpoint to database"""
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
            thread_uuid = UUID(thread_id) if isinstance(thread_id, str) else thread_id
            state_json = json.dumps(state_dict)
            
            await db_adapter.execute_command(
                CREATE_CHECKPOINT,
                checkpoint_id,
                thread_uuid,
                state_json
            )
            
            logger.debug(f"Checkpoint saved for thread {thread_id}")
        except Exception as e:
            logger.error(f"Error saving checkpoint: {str(e)}")
            raise
    
    async def get(
        self,
        config: Dict[str, Any]
    ) -> Optional[Checkpoint]:
        """Load checkpoint from database"""
        try:
            thread_id = config.get("configurable", {}).get("thread_id")
            if not thread_id:
                return None
            
            thread_uuid = UUID(thread_id) if isinstance(thread_id, str) else thread_id
            row = await db_adapter.fetchrow(
                GET_LATEST_CHECKPOINT,
                thread_uuid
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

