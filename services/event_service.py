from EpicEventsCRM.models.employee_model import Employee, DepartmentEnum
from EpicEventsCRM.utils.permissions import has_permission
from EpicEventsCRM.models.contract_model import Contract
from EpicEventsCRM.models.event_model import Event
from db.database import SessionLocal
from auth import get_current_user
from datetime import datetime


def create_event():
    """
    Creates a new event if the user has the necessary permissions.
    """
    current_user = get_current_user()

    if not current_user:
        print("You must be authenticated to create an event.")
        return

    if not has_permission(current_user, 'create_event'):
        print("You do not have permission to create an event.")
        return

    with SessionLocal as session:
        # Selection of the signed contract
        contract_id = input("ID of the signed contract: ")
        contract = session.query(Contract).filter_by(
            contract_id=contract_id, is_signed=True).first()
        if not contract:
            print("Signed contract not found.")
            return

        # Collecting event information
        event_name = input("Event name: ")
        start_date_str = input("Event start date (YYYY-MM-DD HH:MM): ")
        end_date_str = input("Event end date (YYYY-MM-DD HH:MM): ")
        try:
            event_start_date = datetime.strptime(start_date_str, "%Y-%m-%d %H:%M")
            event_end_date = datetime.strptime(end_date_str, "%Y-%m-%d %H:%M")
        except ValueError:
            print("Invalid date format.")
            return

        location = input("Event location: ")
        attendees_input = input("Number of attendees: ")
        try:
            attendees = int(attendees_input)
            if attendees < 0:
                print("Number of participants cannot be negative.")
                return
        except ValueError:
            print("Invalid number of participants.")
            return

        notes = input("Notes (optional): ")

        # Selecting a support contact
        support_employees = session.query(Employee).filter_by(
            department=DepartmentEnum.SUPPORT).all()
        if not support_employees:
            print("No support staff available.")
            return

        print("List of support employees:")
        for emp in support_employees:
            print(f"ID: {emp.employee_id}, Name: {emp.first_name} {emp.last_name}")

        support_contact_id_input = input("ID of the support employee to assign: ")
        try:
            support_contact_id = int(support_contact_id_input)
        except ValueError:
            print("Invalid ID.")
            return

        support_contact = session.query(Employee).filter_by(
            employee_id=support_contact_id, department=DepartmentEnum.SUPPORT).first()
        if not support_contact:
            print("Support employee not found.")
            return

        # Create event without support_contact
        event = Event(
            event_name=event_name,
            event_start_date=event_start_date,
            event_end_date=event_end_date,
            location=location,
            attendees=attendees,
            notes=notes,
            client=contract.client,
            contract=contract,
            support_contact=support_contact
        )

        # Save to database
        session.add(event)
        try:
            session.commit()
            print("Event created successfully.")
        except Exception as e:
            session.rollback()
            print(f"Error creating event: {e}")


def update_event(event_id):
    """
    Updates the information of an event if the user has the necessary permissions.
    """
    current_user = get_current_user()
    if not current_user:
        print("You must be authenticated to update an event.")
        return

    if not has_permission(current_user, 'update_event'):
        print("You do not have permission to update an event.")
        return

    with SessionLocal as session:
        # Retrieve the event
        try:
            event_id = int(event_id)
        except ValueError:
            print("Invalid event ID.")
            return

        event = session.query(Event).filter_by(event_id=event_id).first()
        if not event:
            print("Event not found.")
            return

        # Check if the user is allowed to update this event
        if not has_permission(current_user, 'update_event'):
            print("You do not have permission to update this event.")
            return

        # Collect new information
        print("Leave blank to retain the current value.")
        event_name = input(f"Event name ({event.event_name}): ") or event.event_name

        start_date_str = input(
            f"Start date ({event.event_start_date}) (YYYY-MM-DD HH:MM): ")
        event_start_date = (
            datetime.strptime(start_date_str, "%Y-%m-%d %H:%M")
            if start_date_str else event.event_start_date
        )

        end_date_str = input(f"End date ({event.event_end_date}) (YYYY-MM-DD HH:MM): ")
        event_end_date = (
            datetime.strptime(end_date_str, "%Y-%m-%d %H:%M")
            if end_date_str else event.event_end_date
        )

        location = input(f"Location ({event.location}): ") or event.location

        attendees_input = input(f"Number of attendees ({event.attendees}): ")
        try:
            attendees = int(attendees_input) if attendees_input else event.attendees
            if attendees < 0:
                print("Number of attendees cannot be negative.")
                return
        except ValueError:
            print("Invalid number of attendees.")
            return

        notes = input(f"Notes ({event.notes}): ") or event.notes

        # Update or retain support contact
        print(f"Current support contact: {event.support_contact.first_name} {
              event.support_contact.last_name}")
        update_support_contact = input(
            "Do you want to change the support contact? (Y/N): ").strip().upper()
        if update_support_contact == 'Y':
            support_employees = session.query(Employee).filter_by(
                department=DepartmentEnum.SUPPORT).all()
            if not support_employees:
                print("No support employees available.")
                return

            print("Available support employees:")
            for emp in support_employees:
                print(f"ID: {emp.employee_id}, Name: {emp.first_name} {emp.last_name}")

            support_contact_id_input = input(
                "Enter the ID of the new support contact: ")
            try:
                support_contact_id = int(support_contact_id_input)
            except ValueError:
                print("Invalid support contact ID.")
                return

            support_contact = session.query(Employee).filter_by(
                employee_id=support_contact_id).first()
            if not support_contact:
                print("Support contact not found.")
                return

            event.support_contact = support_contact

        # Update event details
        event.event_name = event_name
        event.event_start_date = event_start_date
        event.event_end_date = event_end_date
        event.location = location
        event.attendees = attendees
        event.notes = notes

        # Save to database
        try:
            session.commit()
            print("Event updated successfully.")
        except Exception as e:
            session.rollback()
            print(f"Error while updating the event: {e}")
