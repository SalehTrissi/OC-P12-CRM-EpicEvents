from sqlalchemy import text
from db.database import session
from sqlalchemy.exc import OperationalError


def test_database_connection():
    """Test if the database connection is working."""
    try:
        session.execute(text("SELECT 1"))
        print("Database connection successful")
        connection_status = True
    except OperationalError:
        print("Database connection failed")
        connection_status = False
    finally:
        session.close()
        print("Database session closed")

    assert connection_status, "Database connection failed"
