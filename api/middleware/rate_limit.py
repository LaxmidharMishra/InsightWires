# api/middleware/rate_limit.py
from fastapi import Request, HTTPException
import time
from collections import defaultdict
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from api.core.config import settings

class RateLimiter(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.requests = defaultdict(list)

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint):
        client_ip = request.client.host
        now = time.time()
        
        # Clean old requests
        self.requests[client_ip] = [
            req_time for req_time in self.requests[client_ip] 
            if req_time > now - 60
        ]
        
        if len(self.requests[client_ip]) >= settings.RATE_LIMIT_PER_MINUTE:
            raise HTTPException(
                status_code=429,
                detail="Too many requests. Please try again later."
            )
            
        self.requests[client_ip].append(now)
        response = await call_next(request)
        return response