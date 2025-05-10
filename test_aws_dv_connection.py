import psycopg2
from psycopg2 import OperationalError

def test_connection():
    try:
        connection = psycopg2.connect(
            host="database-1.cdw2owaw049h.eu-north-1.rds.amazonaws.com",
            port=5432,
            database="insightwiredb",
            user="postgres",
            password="InsightWires2025"
        )
        print("✅ Connection successful!")
        connection.close()
    except OperationalError as e:
        print("❌ Connection failed:")
        print(e)

if __name__ == "__main__":
    test_connection()
