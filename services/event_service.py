from EpicEventsCRM.models.employee_model import Employee, DepartmentEnum
from EpicEventsCRM.utils.permissions import has_permission
from EpicEventsCRM.models.contract_model import Contract
from EpicEventsCRM.models.event_model import Event
from db.database import SessionLocal
from auth import get_current_user
from rich.console import Console
from rich.prompt import Prompt
from datetime import datetime
from rich.panel import Panel
from rich import box


console = Console()


def create_event():
    """
    Creates a new event with a user-friendly and visually appealing interface.
    """
    current_user = get_current_user()

    if not current_user:
        console.print(
            Panel("[bold red]You must be authenticated to create an event.[/bold red]", box=box.ROUNDED))
        return

    if not has_permission(current_user, 'create_event'):
        console.print(
            Panel("[bold red]You do not have permission to create an event.[/bold red]", box=box.ROUNDED))
        return

    console.print(Panel("[bold cyan]Create New Event[/bold cyan]",
                        box=box.ROUNDED, style="bold green"))

    with SessionLocal as session:
        # Select signed contract
        contract_id = Prompt.ask(
            "[bold yellow]Enter ID of the signed contract[/bold yellow]")
        contract = session.query(Contract).filter_by(
            contract_id=contract_id, is_signed=True).first()
        if not contract:
            console.print(
                Panel("[bold red]Signed contract not found.[/bold red]", box=box.ROUNDED))
            return

        # Collect event information
        event_name = Prompt.ask("[bold yellow]Event name[/bold yellow]")
        start_date_str = Prompt.ask(
            "[bold yellow]Event start date (DD-MM-YYYY HH:MM)[/bold yellow]")
        end_date_str = Prompt.ask(
            "[bold yellow]Event end date (DD-MM-YYYY HH:MM)[/bold yellow]")
        try:
            event_start_date = datetime.strptime(start_date_str, "%d-%m-%Y %H:%M")
            event_end_date = datetime.strptime(end_date_str, "%d-%m-%Y %H:%M")
        except ValueError:
            console.print(
                Panel("[bold red]Invalid date format.[/bold red]", box=box.ROUNDED))
            return

        location = Prompt.ask("[bold yellow]Event location[/bold yellow]")
        attendees_input = Prompt.ask("[bold yellow]Number of attendees[/bold yellow]")
        try:
            attendees = int(attendees_input)
            if attendees < 0:
                console.print(
                    Panel("[bold red]Number of participants cannot be negative.[/bold red]", box=box.ROUNDED))
                return
        except ValueError:
            console.print(
                Panel("[bold red]Invalid number of participants.[/bold red]", box=box.ROUNDED))
            return

        notes = Prompt.ask("[bold yellow]Notes (optional)[/bold yellow]", default="")

        # Select support contact
        support_employees = session.query(Employee).filter_by(
            department=DepartmentEnum.SUPPORT).all()
        if not support_employees:
            console.print(
                Panel("[bold red]No support staff available.[/bold red]", box=box.ROUNDED))
            return

        console.print("[bold yellow]List of support employees:[/bold yellow]")
        for emp in support_employees:
            console.print(f"ID: [cyan]{
                          emp.employee_id}[/cyan], Name: [green]{emp.first_name} {emp.last_name}[/green]")

        support_contact_id = Prompt.ask(
            "[bold yellow]ID of the support employee to assign[/bold yellow]")
        support_contact = session.query(Employee).filter_by(
            employee_id=support_contact_id, department=DepartmentEnum.SUPPORT).first()
        if not support_contact:
            console.print(
                Panel("[bold red]Support employee not found.[/bold red]", box=box.ROUNDED))
            return

        # Create event
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
            console.print(
                Panel("[bold green]Event created successfully![/bold green]", box=box.ROUNDED))
        except Exception as e:
            session.rollback()
            console.print(Panel(f"[bold red]Error creating event: {
                          e}[/bold red]", box=box.ROUNDED))


def parse_date(date_str, current_value):
    """
    Parses the input date string or retains the current value if input is blank.
    Handles date strings in both `datetime` and custom format.
    """
    if not date_str.strip():
        return current_value
    try:
        # Attempt to parse the date in the specified format
        return datetime.strptime(date_str, "%d-%m-%Y %H:%M")
    except ValueError as ve:
        # Raise error if parsing fails
        raise ValueError(f"Invalid date format: {ve}")


def update_event(event_id):
    """
    Updates an event with a user-friendly and visually appealing interface.
    """
    current_user = get_current_user()
    if not current_user:
        console.print(
            Panel("[bold red]You must be authenticated to update an event.[/bold red]", box=box.ROUNDED))
        return

    if not has_permission(current_user, 'update_event'):
        console.print(
            Panel("[bold red]You do not have permission to update an event.[/bold red]", box=box.ROUNDED))
        return

    with SessionLocal as session:
        # Retrieve the event
        event = session.query(Event).filter_by(event_id=event_id).first()
        if not event:
            console.print(
                Panel("[bold red]Event not found.[/bold red]", box=box.ROUNDED))
            return

        console.print(Panel(f"[bold cyan]Update Event: {event.event_name}[/bold cyan]",
                            box=box.ROUNDED, style="bold green"))
        console.print(
            "[bold yellow](Leave blank to keep the current value.)[/bold yellow]\n")

        # Collect new information
        event_name = Prompt.ask(
            f"[bold yellow]Event name[/bold yellow] [bold green](current: {
                event.event_name})[/bold green]",
            default=event.event_name,
            show_default=False
        )
        start_date_str = Prompt.ask(
            f"[bold yellow]Start date (DD-MM-YYYY HH:MM)[/bold yellow] [bold green](current: {
                event.event_start_date.strftime('%d-%m-%Y %H:%M')})[/bold green]",
            default=event.event_start_date.strftime("%d-%m-%Y %H:%M"),
            show_default=False
        )
        end_date_str = Prompt.ask(
            f"[bold yellow]End date (DD-MM-YYYY HH:MM)[/bold yellow] [bold green](current: {
                event.event_end_date.strftime('%d-%m-%Y %H:%M')})[/bold green]",
            default=event.event_end_date.strftime("%d-%m-%Y %H:%M"),
            show_default=False
        )
        location = Prompt.ask(
            f"[bold yellow]Location[/bold yellow] [bold green](current: {
                event.location})[/bold green]",
            default=event.location,
            show_default=False
        )
        attendees_input = Prompt.ask(
            f"[bold yellow]Number of attendees[/bold yellow] [bold green](current: {
                event.attendees})[/bold green]",
            default=str(event.attendees),
            show_default=False
        )
        notes = Prompt.ask(
            f"[bold yellow]Notes[/bold yellow] [bold green](current: {
                event.notes})[/bold green]",
            default=event.notes,
            show_default=False
        )

        # Update or retain support contact
        console.print(f"[bold yellow]Current support contact:[/bold yellow] [green]{
                      event.support_contact.first_name} {event.support_contact.last_name}[/green]")
        update_support_contact = Prompt.ask(
            "[bold yellow]Do you want to change the support contact? (Y/N)[/bold yellow]", default="N").upper()
        if update_support_contact == 'Y':
            support_employees = session.query(Employee).filter_by(
                department=DepartmentEnum.SUPPORT).all()
            if not support_employees:
                console.print(
                    Panel("[bold red]No support employees available.[/bold red]", box=box.ROUNDED))
                return

            console.print("[bold yellow]Available support employees:[/bold yellow]")
            for emp in support_employees:
                console.print(f"ID: [cyan]{
                              emp.employee_id}[/cyan], Name: [green]{emp.first_name} {emp.last_name}[/green]")

            support_contact_id = Prompt.ask(
                "[bold yellow]Enter the ID of the new support contact[/bold yellow]")
            support_contact = session.query(Employee).filter_by(
                employee_id=support_contact_id).first()
            if not support_contact:
                console.print(
                    Panel("[bold red]Support contact not found.[/bold red]", box=box.ROUNDED))
                return

            event.support_contact = support_contact

        # Update event details
        try:
            event.event_name = event_name
            event.event_start_date = parse_date(start_date_str, event.event_start_date)
            event.event_end_date = parse_date(end_date_str, event.event_end_date)
            event.location = location
            event.attendees = int(attendees_input)
            event.notes = notes

            session.commit()
            console.print(
                Panel("[bold green]Event updated successfully![/bold green]", box=box.ROUNDED))
        except ValueError as ve:
            console.print(
                Panel(f"[bold red]Error: {ve}[/bold red]", box=box.ROUNDED))
        except Exception as e:
            session.rollback()
            console.print(Panel(f"[bold red]Error updating event: {
                          e}[/bold red]", box=box.ROUNDED))
