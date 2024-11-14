from EpicEventsCRM.utils.permissions import has_permission
from EpicEventsCRM.models.contract_model import Contract
from EpicEventsCRM.models.client_model import Client
from EpicEventsCRM.models.event_model import Event
from db.database import SessionLocal
from auth import get_current_user


def get_all_clients():
    """
    Retrieves all clients if the user is authenticated and has the necessary permissions.
    """
    user = get_current_user()
    if not user:
        print("You must be authenticated to access clients.")
        return []

    if not has_permission(user, 'read_clients'):
        print("You do not have permission to access clients.")
        return []

    with SessionLocal as session:
        clients = session.query(Client).all()
        return clients


def get_all_contracts():
    """
    Get all contracts if the user is authenticated and has the necessary permissions.
    """
    user = get_current_user()
    if not user:
        print("You must be authenticated to access contracts.")
        return []

    if not has_permission(user, 'read_contracts'):
        print("You do not have permission to access contracts.")
        return []

    with SessionLocal as session:
        contracts = session.query(Contract).all()
        return contracts


def get_all_events():
    """
    Get all events if the user is authenticated and has the necessary permissions.
    """
    user = get_current_user()
    if not user:
        print("You must be authenticated to access events.")
        return []

    if not has_permission(user, 'read_events'):
        print("You do not have permission to access events.")
        return []

    with SessionLocal as session:
        events = session.query(Event).all()
        return events
