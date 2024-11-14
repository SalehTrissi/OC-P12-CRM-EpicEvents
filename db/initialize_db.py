import os
import sys

# Add project root directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def initialize_database():
    """Create all tables in the database."""

    from database import engine
    from EpicEventsCRM.models.base_model import Base
    from EpicEventsCRM.models.client_model import Client  # noqa
    from EpicEventsCRM.models.contract_model import Contract  # noqa
    from EpicEventsCRM.models.employee_model import Employee  # noqa
    from EpicEventsCRM.models.event_model import Event  # noqa

    Base.metadata.create_all(bind=engine)
    print("All tables have been created successfully.")


if __name__ == "__main__":
    initialize_database()
