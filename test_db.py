# test_db.py
import asyncio
import sys
import platform
from sqlalchemy import select, text
from util.database import AsyncSessionLocal

# Fix for Windows ProactorEventLoop SSL issue
if platform.system() == 'Windows':
    try:
        from asyncio import WindowsSelectorEventLoopPolicy
        asyncio.set_event_loop_policy(WindowsSelectorEventLoopPolicy())
    except Exception as e:
        print(f"Warning: Could not set Windows event loop policy: {e}")

async def test_connection():
    session = None
    try:
        session = AsyncSessionLocal()
        # Try a simple query to verify connection using text()
        result = await session.execute(text("SELECT 1"))
        print("Database connection successful!")
        
        # Test querying a table using text()
        result = await session.execute(text("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
        """))
        tables = result.fetchall()
        
        print("\nAvailable tables:")
        for table in tables:
            print(f"- {table[0]}")
            
        # Try to query news_metadata table
        print(f"\nSample data from news_metadata:")
        result = await session.execute(
            text("SELECT * FROM news_metadata LIMIT 3")
        )
        rows = result.fetchall()
        for row in rows:
            print(row)

        await session.commit()

    except Exception as e:
        print(f"Error connecting to database: {e}")
        if session:
            await session.rollback()
        raise e
    finally:
        if session:
            await session.close()

async def main():
    print("Testing database connection...")
    try:
        await test_connection()
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Clean up any remaining tasks
        tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
        for task in tasks:
            task.cancel()
        await asyncio.gather(*tasks, return_exceptions=True)

def run_test():
    try:
        if sys.version_info >= (3, 7):
            asyncio.run(main())
        else:
            loop = asyncio.get_event_loop()
            try:
                loop.run_until_complete(main())
            finally:
                loop.close()
    except KeyboardInterrupt:
        print("\nTest interrupted by user")
    except Exception as e:
        print(f"\nUnexpected error: {e}")

if __name__ == "__main__":
    run_test()