# api/core/cache.py
from functools import wraps
from cachetools import TTLCache
from api.core.config import settings
from typing import Optional, Callable, Any
import hashlib
import json

# Create cache instances with different TTLs
caches = {
    'default': TTLCache(maxsize=settings.CACHE_CONFIG['max_size'], ttl=settings.CACHE_CONFIG['default_ttl']),
    'short': TTLCache(maxsize=settings.CACHE_CONFIG['max_size'], ttl=settings.CACHE_CONFIG['short_ttl']),
    'medium': TTLCache(maxsize=settings.CACHE_CONFIG['max_size'], ttl=settings.CACHE_CONFIG['medium_ttl']),
    'long': TTLCache(maxsize=settings.CACHE_CONFIG['max_size'], ttl=settings.CACHE_CONFIG['long_ttl'])
}

def cache_response(cache_type: str = 'default', cache_key: Optional[str] = None):
    """
    Cache decorator for API responses
    
    Args:
        cache_type: Type of cache to use ('default', 'short', 'medium', 'long')
        cache_key: Optional custom cache key
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs) -> Any:
            # Get the appropriate cache
            cache = caches.get(cache_type, caches['default'])
            
            # Generate cache key if not provided
            if cache_key:
                key = cache_key
            else:
                # Create a deterministic key from function name and arguments
                key_parts = [func.__name__]
                if args:
                    key_parts.extend([str(arg) for arg in args])
                if kwargs:
                    # Sort kwargs to ensure consistent key generation
                    sorted_kwargs = sorted(kwargs.items())
                    key_parts.extend([f"{k}={v}" for k, v in sorted_kwargs])
                
                key_string = ":".join(key_parts)
                key = hashlib.md5(key_string.encode()).hexdigest()
            
            # Check cache
            if key in cache:
                return cache[key]
            
            # Execute function and cache result
            result = await func(*args, **kwargs)
            cache[key] = result
            return result
        return wrapper
    return decorator