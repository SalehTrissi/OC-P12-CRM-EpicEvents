import os
import sys

# Ensure the project root is accessible
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


def initialize_database():
    """Create all tables in the database."""

    from db.database import engine
    from EpicEventsCRM.models.base_model import Base
    from EpicEventsCRM.models.client_model import Client  # noqa
    from EpicEventsCRM.models.contract_model import Contract  # noqa
    from EpicEventsCRM.models.employee_model import Employee  # noqa
    from EpicEventsCRM.models.event_model import Event  # noqa

    try:
        Base.metadata.create_all(bind=engine)
        print("✅ All tables have been created successfully.")
    except Exception as e:
        print(f"❌ Error initializing database: {e}")


if __name__ == "__main__":
    initialize_database()
