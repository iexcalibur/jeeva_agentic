"""Run database migrations"""
import asyncio
from scripts.init_db import main
from app.core.logging import logger


if __name__ == "__main__":
    logger.info("Running database migrations...")
    asyncio.run(main())

