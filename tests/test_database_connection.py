from sqlalchemy import text
from db.database import get_db
from sqlalchemy.exc import OperationalError


def test_database_connection():
    """Test if the database connection is working."""
    connection_status = False
    db = next(get_db())

    try:
        print("Attempting to execute a test query...")
        db.execute(text("SELECT 1"))
        print("✅ Database connection successful")
        connection_status = True
    except OperationalError as e:
        print(f"❌ Database connection failed: {e}")
        connection_status = False
    finally:
        db.close()
        print("🔄 Database session closed")

    assert connection_status, "❌ Database connection failed"


# Directly call the function
print("🏁 Running database connection test...")
test_database_connection()
