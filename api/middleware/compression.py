# api/middleware/compression.py
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import Response, StreamingResponse
import gzip

class CompressionMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint):
        response = await call_next(request)
        
        if "gzip" in request.headers.get("Accept-Encoding", "").lower():
            # Handle StreamingResponse differently
            if isinstance(response, StreamingResponse):
                return response
            
            # For regular responses
            if hasattr(response, 'body') and isinstance(response.body, bytes):
                compressed_body = gzip.compress(response.body)
                return Response(
                    content=compressed_body,
                    status_code=response.status_code,
                    headers={
                        **response.headers,
                        "Content-Encoding": "gzip",
                        "Content-Length": str(len(compressed_body))
                    }
                )
        
        return response