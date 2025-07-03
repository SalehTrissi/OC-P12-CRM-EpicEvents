# File: services/data_access.py (Refactored)

from EpicEventsCRM.models.employee_model import Employee
from EpicEventsCRM.utils.permissions import has_permission
from EpicEventsCRM.models.contract_model import Contract
from EpicEventsCRM.models.client_model import Client
from EpicEventsCRM.models.event_model import Event
from sqlalchemy.orm import joinedload
from functools import wraps
from auth import get_current_user
from db.database import get_db
import sentry_sdk


def require_permission(permission_name: str):
    """
    A decorator that checks if a user is authenticated and has the required permission.
    Handles exceptions and Sentry logging for authorization failures.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            user = get_current_user()
            if not user:
                sentry_sdk.capture_message(
                    f"Unauthorized access attempt to {func.__name__}", level="warning"
                )
                raise PermissionError("Authentication required. Please log in.")

            if not has_permission(user, permission_name):
                sentry_sdk.capture_message(
                    f"User '{user.email}' lacks permission for '{permission_name}'.",
                    level="warning",
                )
                raise PermissionError(
                    "You do not have permission to perform this action."
                )

            # If checks pass, execute the original function
            return func(*args, **kwargs)
        return wrapper
    return decorator


@require_permission("list_clients")
def get_all_clients():
    """Retrieves all clients from the database with their sales contact."""
    db = next(get_db())
    try:
        return db.query(Client).options(joinedload(Client.sales_contact)).all()
    except Exception as e:
        sentry_sdk.capture_exception(e)
        raise RuntimeError(f"Database error while retrieving clients: {e}")
    finally:
        db.close()


@require_permission("list_contracts")
def get_all_contracts(not_signed: bool = False, not_paid: bool = False):
    """Retrieves all contracts from the database, with optional filters."""
    db = next(get_db())
    try:
        query = db.query(Contract).options(
            joinedload(Contract.client), joinedload(Contract.sales_contact)
        )
        if not_signed:
            query = query.filter(Contract.is_signed.is_(False))
        if not_paid:
            query = query.filter(Contract.remaining_amount > 0)

        return query.order_by(Contract.contract_id).all()
    except Exception as e:
        sentry_sdk.capture_exception(e)
        raise RuntimeError(f"Database error while retrieving contracts: {e}")
    finally:
        db.close()


@require_permission("list_events")
def get_all_events(no_support: bool = False, my_events: bool = False):
    """Retrieves all events from the database, with optional filters."""
    db = next(get_db())
    try:
        query = db.query(Event).options(
            joinedload(Event.client), joinedload(Event.support_contact)
        )

        if no_support:
            query = query.filter(Event.support_contact_id.is_(None))

        if my_events:
            current_user = get_current_user()
            if not current_user:
                raise PermissionError("Authentication required to view your events.")
            query = query.filter(Event.support_contact_id == current_user.employee_id)

        return query.order_by(Event.event_start_date).all()

    except Exception as e:
        sentry_sdk.capture_exception(e)
        raise RuntimeError(f"Database error while retrieving events: {e}")
    finally:
        db.close()


@require_permission("list_employees")
def get_all_employees():
    """Retrieves all employees from the database."""
    db = next(get_db())
    try:
        return db.query(Employee).all()
    except Exception as e:
        sentry_sdk.capture_exception(e)
        raise RuntimeError(f"Database error while retrieving employees: {e}")
    finally:
        db.close()
