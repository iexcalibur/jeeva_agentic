"""Seed test data (optional)"""
import asyncio
from uuid import uuid4
from app.database.connection import create_pool, close_pool, get_connection
from app.services.memory.thread_manager import ThreadManager
from app.core.logging import logger


async def seed_data():
    """Seed database with test data"""
    try:
        logger.info("Seeding test data...")
        manager = ThreadManager()
        
        # Create test user and thread
        user_id = str(uuid4())
        thread = await manager.create_thread(
            user_id=user_id,
            persona="business_expert"
        )
        
        # Add some test messages
        await manager.save_message(
            thread_id=str(thread.thread_id),
            role="user",
            content="Hello, I need help with my business strategy"
        )
        
        await manager.save_message(
            thread_id=str(thread.thread_id),
            role="assistant",
            content="I'd be happy to help you with your business strategy. What specific area would you like to focus on?"
        )
        
        logger.info(f"Seeded test data for user {user_id}")
        logger.info(f"Thread ID: {thread.thread_id}")
        
    except Exception as e:
        logger.error(f"Error seeding data: {str(e)}")
        raise


async def main():
    """Main seeding function"""
    try:
        await create_pool()
        await seed_data()
    except Exception as e:
        logger.error(f"Error in seed script: {str(e)}")
        raise
    finally:
        await close_pool()


if __name__ == "__main__":
    asyncio.run(main())

