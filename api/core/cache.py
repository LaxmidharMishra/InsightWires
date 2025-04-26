# api/core/cache.py
from functools import wraps
from cachetools import TTLCache
from api.core.config import settings

# Create cache instances
metadata_cache = TTLCache(maxsize=100, ttl=settings.CACHE_TTL)

def cache_response(cache_key: str = None):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Generate cache key if not provided
            key = cache_key or f"{func.__name__}:{str(args)}:{str(kwargs)}"
            
            # Check cache
            if key in metadata_cache:
                return metadata_cache[key]
            
            # Execute function and cache result
            result = await func(*args, **kwargs)
            metadata_cache[key] = result
            return result
        return wrapper
    return decorator