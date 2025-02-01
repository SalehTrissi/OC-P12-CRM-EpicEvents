from EpicEventsCRM.utils.permissions import has_permission
from EpicEventsCRM.models.contract_model import Contract
from EpicEventsCRM.models.client_model import Client
from EpicEventsCRM.models.event_model import Event
from sqlalchemy.orm import joinedload
from auth import get_current_user
from db.database import get_db
import sentry_sdk


def get_all_clients():
    """
    Retrieves all clients if the user is authenticated and has the necessary
    permissions. Includes sales contact details using `joinedload`.
    """
    user = get_current_user()
    if not user:
        sentry_sdk.capture_message(
            "Unauthorized access attempt to get_all_clients", level="warning"
        )
        raise PermissionError("Authentication required. Please login.")

    if not has_permission(user, "list_clients"):
        sentry_sdk.capture_message(
            f"User '{user.email}' lacks permission to view clients.", level="warning"
        )
        raise PermissionError("You do not have permission to view clients.")

    db = next(get_db())
    try:
        clients = db.query(Client).options(joinedload(Client.sales_contact)).all()
        return clients
    except Exception as e:
        sentry_sdk.capture_exception(e)
        raise RuntimeError(f"Error retrieving clients: {e}")
    finally:
        db.close()


def get_all_contracts():
    """
    Retrieves all contracts if the user is authenticated and has the necessary
    permissions. Includes client and sales contact details using `joinedload`.
    """
    user = get_current_user()
    if not user:
        sentry_sdk.capture_message(
            "Unauthorized access attempt to get_all_contracts", level="warning"
        )
        raise PermissionError("Authentication required. Please login.")

    if not has_permission(user, "list_contracts"):
        sentry_sdk.capture_message(
            f"User '{user.email}' lacks permission to view contracts.", level="warning"
        )
        raise PermissionError("You do not have permission to view contracts.")

    db = next(get_db())
    try:
        contracts = (
            db.query(Contract)
            .options(joinedload(Contract.client), joinedload(Contract.sales_contact))
            .all()
        )
        return contracts
    except Exception as e:
        sentry_sdk.capture_exception(e)
        raise RuntimeError(f"Error retrieving contracts: {e}")
    finally:
        db.close()


def get_all_events():
    """
    Retrieves all events if the user is authenticated and has the necessary permissions.
    Includes client and support contact details using `joinedload`.
    """
    user = get_current_user()
    if not user:
        sentry_sdk.capture_message(
            "Unauthorized access attempt to get_all_events", level="warning"
        )
        raise PermissionError("Authentication required. Please login.")

    if not has_permission(user, "list_events"):
        sentry_sdk.capture_message(
            f"User '{user.email}' lacks permission to view events.", level="warning"
        )
        raise PermissionError("You do not have permission to view events.")

    db = next(get_db())
    try:
        events = (
            db.query(Event)
            .options(joinedload(Event.client), joinedload(Event.support_contact))
            .all()
        )
        return events
    except Exception as e:
        sentry_sdk.capture_exception(e)
        raise RuntimeError(f"Error retrieving events: {e}")
    finally:
        db.close()
