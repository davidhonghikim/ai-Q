# AI-Q Knowledge Library System - Cache Service
# TOKEN COUNT: ~1,100 tokens
"""
Cache service for AI-Q Knowledge Library System.
Handles Redis cache initialization and management.
"""

import asyncio
import json
import logging
from typing import Any, Optional, Union
from datetime import timedelta

import redis.asyncio as redis
from src.config.settings import get_settings

# Configure logging
logger = logging.getLogger(__name__)

class CacheService:
    """Cache service for managing Redis operations."""
    
    def __init__(self):
        self.settings = get_settings()
        self.redis_client: Optional[redis.Redis] = None
        self._connection_pool: Optional[redis.ConnectionPool] = None
    
    async def initialize(self) -> None:
        """Initialize Redis connection and test connectivity."""
        try:
            logger.info("Initializing cache service...")
            
            # Create connection pool
            self._connection_pool = redis.ConnectionPool(
                host=self.settings.database.redis.host,
                port=self.settings.database.redis.port,
                password=self.settings.database.redis.password or None,
                db=self.settings.database.redis.database,
                decode_responses=True,
                max_connections=20,
                retry_on_timeout=True,
                health_check_interval=30
            )
            
            # Create Redis client
            self.redis_client = redis.Redis(connection_pool=self._connection_pool)
            
            # Test connection
            await self._test_connection()
            
            logger.info("Cache service initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize cache service: {e}")
            raise
    
    async def _test_connection(self) -> None:
        """Test Redis connection."""
        try:
            await self.redis_client.ping()
            logger.info("Redis connection test successful")
        except Exception as e:
            logger.error(f"Redis connection test failed: {e}")
            raise
    
    async def set(self, key: str, value: Any, expire: Optional[timedelta] = None) -> bool:
        """Set a key-value pair in cache."""
        try:
            if isinstance(value, (dict, list)):
                value = json.dumps(value)
            
            result = await self.redis_client.set(key, value)
            
            if expire:
                await self.redis_client.expire(key, int(expire.total_seconds()))
            
            return result
        except Exception as e:
            logger.error(f"Failed to set cache key {key}: {e}")
            return False
    
    async def get(self, key: str) -> Optional[Any]:
        """Get a value from cache."""
        try:
            value = await self.redis_client.get(key)
            if value is None:
                return None
            
            # Try to parse as JSON
            try:
                return json.loads(value)
            except json.JSONDecodeError:
                return value
                
        except Exception as e:
            logger.error(f"Failed to get cache key {key}: {e}")
            return None
    
    async def delete(self, key: str) -> bool:
        """Delete a key from cache."""
        try:
            result = await self.redis_client.delete(key)
            return result > 0
        except Exception as e:
            logger.error(f"Failed to delete cache key {key}: {e}")
            return False
    
    async def exists(self, key: str) -> bool:
        """Check if a key exists in cache."""
        try:
            result = await self.redis_client.exists(key)
            return result > 0
        except Exception as e:
            logger.error(f"Failed to check cache key {key}: {e}")
            return False
    
    async def expire(self, key: str, expire: timedelta) -> bool:
        """Set expiration for a key."""
        try:
            result = await self.redis_client.expire(key, int(expire.total_seconds()))
            return result
        except Exception as e:
            logger.error(f"Failed to set expiration for cache key {key}: {e}")
            return False
    
    async def clear_pattern(self, pattern: str) -> int:
        """Clear all keys matching a pattern."""
        try:
            keys = await self.redis_client.keys(pattern)
            if keys:
                result = await self.redis_client.delete(*keys)
                logger.info(f"Cleared {result} keys matching pattern: {pattern}")
                return result
            return 0
        except Exception as e:
            logger.error(f"Failed to clear cache pattern {pattern}: {e}")
            return 0
    
    async def get_stats(self) -> dict:
        """Get cache statistics."""
        try:
            info = await self.redis_client.info()
            return {
                "connected_clients": info.get("connected_clients", 0),
                "used_memory_human": info.get("used_memory_human", "0B"),
                "total_commands_processed": info.get("total_commands_processed", 0),
                "keyspace_hits": info.get("keyspace_hits", 0),
                "keyspace_misses": info.get("keyspace_misses", 0)
            }
        except Exception as e:
            logger.error(f"Failed to get cache stats: {e}")
            return {}
    
    async def close(self) -> None:
        """Close Redis connections."""
        try:
            if self.redis_client:
                await self.redis_client.close()
            if self._connection_pool:
                await self._connection_pool.disconnect()
            logger.info("Cache connections closed")
        except Exception as e:
            logger.error(f"Error closing cache connections: {e}")

# Global cache service instance
_cache_service: Optional[CacheService] = None

async def init_cache() -> None:
    """Initialize the cache service."""
    global _cache_service
    
    try:
        _cache_service = CacheService()
        await _cache_service.initialize()
        logger.info("Cache initialization completed")
    except Exception as e:
        logger.error(f"Cache initialization failed: {e}")
        raise

async def get_cache_service() -> CacheService:
    """Get the cache service instance."""
    if not _cache_service:
        raise RuntimeError("Cache service not initialized")
    return _cache_service

async def close_cache() -> None:
    """Close cache connections."""
    global _cache_service
    if _cache_service:
        await _cache_service.close()
        _cache_service = None 