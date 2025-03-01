import sys
sys.path.append("/app")
import logging
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from api.endpoints import router as news_router
import uvicorn
from mangum import Mangum

# Logging configuration
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger("InsightWiresFastApi")

app = FastAPI(title="Insight Wires News API", version="1.0", description="News Search API")
handler = Mangum(app)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register endpoints
app.include_router(news_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
