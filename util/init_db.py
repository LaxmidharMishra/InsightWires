import asyncio
import logging
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from api.models import Base
import os
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

async def init_db():
    try:
        # Get database URL from environment variable
        database_url = os.getenv("DATABASE_URL")
        if not database_url:
            raise ValueError("DATABASE_URL environment variable is not set")

        logger.info("Creating database engine...")
        engine = create_async_engine(database_url, echo=True)
        
        logger.info("Creating database tables...")
        async with engine.begin() as conn:
            # Drop all tables first
            logger.info("Dropping existing tables...")
            await conn.run_sync(Base.metadata.drop_all)
            
            # Create all tables
            logger.info("Creating new tables...")
            await conn.run_sync(Base.metadata.create_all)
        
        logger.info("Database initialization completed successfully!")
        
    except Exception as e:
        logger.error(f"Error initializing database: {str(e)}")
        raise

if __name__ == "__main__":
    asyncio.run(init_db()) 