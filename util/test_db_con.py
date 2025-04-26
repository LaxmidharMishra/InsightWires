import asyncpg
import asyncio

DATABASE_URL = "postgresql://insightwireadmin:InsightWire_JPL_2025@insightwiresfinal.c7yekk48a7a7.eu-north-1.rds.amazonaws.com:5432/news_analytics"

async def test_connection():
    try:
        conn = await asyncpg.connect(DATABASE_URL)
        print("✅ Successfully connected to AWS RDS PostgreSQL!")
        await conn.close()
    except Exception as e:
        print(f"❌ Connection failed: {e}")

asyncio.run(test_connection())
