# api/core/config.py
from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import List, Optional

class Settings(BaseSettings):
    # API Settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Insight Wires API"
    
    # Database
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: str
    POSTGRES_DB: str
    DATABASE_URL: Optional[str] = None  # Make this optional

    # Security
    SECRET_KEY: str
    API_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 60
    
    # CORS
    ALLOWED_ORIGINS: str = "http://localhost:3000"
    
    # Cache
    CACHE_TTL: int = 300  # 5 minutes

    class Config:
        env_file = ".env"

    def model_post_init(self, _context):
        # Move the DATABASE_URL construction to post_init
        if not self.DATABASE_URL:
            self.DATABASE_URL = (
                f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
                f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
            )
        # Convert ALLOWED_ORIGINS string to list
        self.ALLOWED_ORIGINS = [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",")]

@lru_cache()
def get_settings():
    return Settings()

settings = get_settings()

# For testing
if __name__ == "__main__":
    print(settings.dict())