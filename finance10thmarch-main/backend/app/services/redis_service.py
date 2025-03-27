import json
import hashlib
from typing import Dict, Any, Optional
import redis
from app.core.config import REDIS_HOST, REDIS_PORT, REDIS_PASSWORD

class RedisService:
    def __init__(self):
        """Initialize Redis connection"""
        try:
            self.redis_client = redis.Redis(
                host=REDIS_HOST,
                port=int(REDIS_PORT),
                password=REDIS_PASSWORD,
                decode_responses=True
            )
            self.enabled = True
        except Exception as e:
            print(f"Redis connection failed: {e}")
            self.enabled = False
    
    def _get_cache_key(self, prefix: str, query: str) -> str:
        """
        Generate a cache key for a query
        
        Args:
            prefix (str): Key prefix
            query (str): Query string
            
        Returns:
            str: Cache key
        """
        # Normalize query (lowercase, remove extra spaces)
        normalized_query = ' '.join(query.lower().split())
        
        # Create a hash of the query for a shorter key
        query_hash = hashlib.md5(normalized_query.encode()).hexdigest()
        
        return f"{prefix}:{query_hash}"
    
    async def get_api_plan(self, query: str) -> Optional[Dict[str, Any]]:
        """
        Get a cached API plan for a query
        
        Args:
            query (str): User query
            
        Returns:
            Optional[Dict[str, Any]]: Cached API plan or None
        """
        if not self.enabled:
            return None
        
        try:
            cache_key = self._get_cache_key("api_plan", query)
            cached_data = self.redis_client.get(cache_key)
            
            if cached_data:
                return json.loads(cached_data)
            
            return None
        except Exception as e:
            print(f"Redis get error: {e}")
            return None
    
    async def set_api_plan(self, query: str, api_plan: Dict[str, Any], expire_seconds: int = 3600) -> bool:
        """
        Cache an API plan for a query
        
        Args:
            query (str): User query
            api_plan (Dict[str, Any]): API plan to cache
            expire_seconds (int): Cache expiration time in seconds
            
        Returns:
            bool: Success status
        """
        if not self.enabled:
            return False
        
        try:
            cache_key = self._get_cache_key("api_plan", query)
            self.redis_client.setex(
                cache_key,
                expire_seconds,
                json.dumps(api_plan)
            )
            return True
        except Exception as e:
            print(f"Redis set error: {e}")
            return False
    
    async def get_query_response(self, query: str) -> Optional[Dict[str, Any]]:
        """
        Get a cached query response
        
        Args:
            query (str): User query
            
        Returns:
            Optional[Dict[str, Any]]: Cached response or None
        """
        if not self.enabled:
            return None
        
        try:
            cache_key = self._get_cache_key("query_response", query)
            cached_data = self.redis_client.get(cache_key)
            
            if cached_data:
                return json.loads(cached_data)
            
            return None
        except Exception as e:
            print(f"Redis get error: {e}")
            return None
    
    async def set_query_response(self, query: str, response: Dict[str, Any], expire_seconds: int = 1800) -> bool:
        """
        Cache a query response
        
        Args:
            query (str): User query
            response (Dict[str, Any]): Response to cache
            expire_seconds (int): Cache expiration time in seconds
            
        Returns:
            bool: Success status
        """
        if not self.enabled:
            return False
        
        try:
            cache_key = self._get_cache_key("query_response", query)
            self.redis_client.setex(
                cache_key,
                expire_seconds,
                json.dumps(response)
            )
            return True
        except Exception as e:
            print(f"Redis set error: {e}")
            return False 