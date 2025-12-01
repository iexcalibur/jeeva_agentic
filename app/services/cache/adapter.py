"""Cache adapter supporting both in-memory and Redis"""
from typing import Optional, Any
import json
from app.core.config import settings
from app.core.logging import logger


class CacheAdapter:
    """Adapter for caching operations supporting in-memory and Redis"""
    
    def __init__(self):
        self.cache_type = settings.CACHE_TYPE
        self._memory_cache: dict = {}
        self._redis_client: Optional[Any] = None
    
    async def initialize(self):
        """Initialize cache backend"""
        if self.cache_type == "redis":
            try:
                import redis.asyncio as redis
                self._redis_client = await redis.from_url(
                    f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/{settings.REDIS_DB}",
                    password=settings.REDIS_PASSWORD,
                    decode_responses=True
                )
                # Test connection
                await self._redis_client.ping()
                logger.info("Redis cache initialized")
            except ImportError:
                logger.warning("redis package not installed, falling back to in-memory cache")
                self.cache_type = "memory"
                self._memory_cache = {}
            except Exception as e:
                logger.warning(f"Failed to connect to Redis: {str(e)}, falling back to in-memory cache")
                self.cache_type = "memory"
                self._memory_cache = {}
        else:
            logger.info("Using in-memory cache")
    
    async def close(self):
        """Close cache connections"""
        if self._redis_client:
            await self._redis_client.close()
            logger.info("Redis connection closed")
    
    async def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        try:
            if self.cache_type == "redis" and self._redis_client:
                value = await self._redis_client.get(key)
                if value:
                    return json.loads(value)
                return None
            else:
                return self._memory_cache.get(key)
        except Exception as e:
            logger.error(f"Error getting cache key {key}: {str(e)}")
            return None
    
    async def set(self, key: str, value: Any, ttl: Optional[int] = None):
        """Set value in cache"""
        try:
            if self.cache_type == "redis" and self._redis_client:
                serialized = json.dumps(value)
                if ttl:
                    await self._redis_client.setex(key, ttl, serialized)
                else:
                    await self._redis_client.set(key, serialized)
            else:
                self._memory_cache[key] = value
        except Exception as e:
            logger.error(f"Error setting cache key {key}: {str(e)}")
    
    async def delete(self, key: str):
        """Delete key from cache"""
        try:
            if self.cache_type == "redis" and self._redis_client:
                await self._redis_client.delete(key)
            else:
                self._memory_cache.pop(key, None)
        except Exception as e:
            logger.error(f"Error deleting cache key {key}: {str(e)}")
    
    async def clear(self):
        """Clear all cache"""
        try:
            if self.cache_type == "redis" and self._redis_client:
                await self._redis_client.flushdb()
            else:
                self._memory_cache.clear()
        except Exception as e:
            logger.error(f"Error clearing cache: {str(e)}")


# Global cache adapter instance
cache_adapter = CacheAdapter()

