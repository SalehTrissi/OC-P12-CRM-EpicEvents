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
        raise PermissionError("Authentication required. Please login.")

    if not has_permission(user, 'read_clients'):
        raise PermissionError("You do not have permission to view clients.")

    with SessionLocal as session:
        return session.query(Client).all()


def get_all_contracts():
    """
    Retrieves all contracts if the user is authenticated and has the necessary permissions.
    """
    user = get_current_user()
    if not user:
        raise PermissionError("Authentication required. Please login.")

    if not has_permission(user, 'read_contracts'):
        raise PermissionError("You do not have permission to view contracts.")

    with SessionLocal as session:
        return session.query(Contract).all()


def get_all_events():
    """
    Retrieves all events if the user is authenticated and has the necessary permissions.
    """
    user = get_current_user()
    if not user:
        raise PermissionError("Authentication required. Please login.")

    if not has_permission(user, 'read_events'):
        raise PermissionError("You do not have permission to view events.")

    with SessionLocal as session:
        return session.query(Event).all()
