from EpicEventsCRM.models.employee_model import Employee, DepartmentEnum
from EpicEventsCRM.utils.permissions import has_permission
from EpicEventsCRM.models.contract_model import Contract
from EpicEventsCRM.models.event_model import Event
from auth import get_current_user
from rich.console import Console
from rich.prompt import Prompt
from db.database import get_db
from datetime import datetime
from rich.panel import Panel
from rich import box
import sentry_sdk


console = Console()


def parse_date(date_str, current_value=None):
    """Parse a date string or retain the current value if input is blank."""
    if not date_str.strip():
        return current_value
    try:
        return datetime.strptime(date_str, "%d-%m-%Y %H:%M")
    except ValueError as ve:
        raise ValueError(f"Invalid date format: {ve}")


def create_event():
    """Create a new event with an interactive interface."""
    current_user = get_current_user()

    if not current_user:
        console.print(
            Panel("[bold red]Authentication required.[/bold red]", box=box.ROUNDED)
        )
        return

    if not has_permission(current_user, "create_event"):
        console.print(
            Panel("[bold red]Insufficient permissions.[/bold red]", box=box.ROUNDED)
        )
        return

    console.print(
        Panel(
            "[bold cyan]Create New Event[/bold cyan]",
            box=box.ROUNDED,
            style="bold green",
        )
    )

    db = next(get_db())

    try:
        contract_id = Prompt.ask(
            "[bold yellow]Enter ID of the signed contract[/bold yellow]"
        )
        contract = (
            db.query(Contract)
            .filter_by(contract_id=contract_id, is_signed=True)
            .first()
        )

        if not contract:
            console.print(
                Panel(
                    "[bold red]Signed contract not found.[/bold red]", box=box.ROUNDED
                )
            )
            return

        event_name = Prompt.ask("[bold yellow]Event name[/bold yellow]")
        start_date_str = Prompt.ask(
            "[bold yellow]Start date (DD-MM-YYYY HH:MM)[/bold yellow]"
        )
        end_date_str = Prompt.ask(
            "[bold yellow]End date (DD-MM-YYYY HH:MM)[/bold yellow]"
        )
        event_start_date = parse_date(start_date_str)
        event_end_date = parse_date(end_date_str)

        location = Prompt.ask("[bold yellow]Event location[/bold yellow]")
        attendees = Prompt.ask(
            "[bold yellow]Number of attendees[/bold yellow]", default="0"
        )

        try:
            attendees = int(attendees)
            if attendees < 0:
                raise ValueError("Number of attendees cannot be negative.")
        except ValueError as e:
            console.print(Panel(f"[bold red]{e}[/bold red]", box=box.ROUNDED))
            return

        notes = Prompt.ask("[bold yellow]Notes (optional)[/bold yellow]", default="")

        # Get support contact
        support_employees = (
            db.query(Employee).filter_by(department=DepartmentEnum.SUPPORT).all()
        )

        if not support_employees:
            console.print(
                Panel(
                    "[bold red]No support staff available.[/bold red]", box=box.ROUNDED
                )
            )
            return

        console.print("[bold yellow]Available support employees:[/bold yellow]")
        for emp in support_employees:
            console.print(
                f"ID: [cyan]{
                    emp.employee_id}[/cyan], Name: [green]{
                        emp.first_name} {emp.last_name}[/green]"
            )

        support_contact_id = Prompt.ask(
            "[bold yellow]Enter support employee ID[/bold yellow]"
        )
        support_contact = (
            db.query(Employee)
            .filter_by(
                employee_id=support_contact_id, department=DepartmentEnum.SUPPORT
            )
            .first()
        )

        if not support_contact:
            console.print(
                Panel(
                    "[bold red]Support employee not found.[/bold red]", box=box.ROUNDED
                )
            )
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
            support_contact=support_contact,
        )

        db.add(event)
        db.commit()

        console.print(
            Panel(
                "[bold green]Event created successfully![/bold green]", box=box.ROUNDED
            )
        )
        sentry_sdk.capture_message(
            f"Event '{event_name}' created successfully!", level="info"
        )

    except ValueError as ve:
        console.print(Panel(f"[bold red]Error: {ve}[/bold red]", box=box.ROUNDED))
    except Exception as e:
        db.rollback()
        console.print(
            Panel(
                f"[bold red]Unexpected error: {
                    e}[/bold red]",
                box=box.ROUNDED,
            )
        )
        sentry_sdk.capture_exception(e)
    finally:
        db.close()


def update_event(event_id):
    """Update an existing event."""
    current_user = get_current_user()

    if not current_user:
        console.print(
            Panel("[bold red]Authentication required.[/bold red]", box=box.ROUNDED)
        )
        return

    if not has_permission(current_user, "update_event"):
        console.print(
            Panel("[bold red]Insufficient permissions.[/bold red]", box=box.ROUNDED)
        )
        return

    db = next(get_db())

    try:
        event = db.query(Event).filter_by(event_id=event_id).first()

        if not event:
            console.print(
                Panel("[bold red]Event not found.[/bold red]", box=box.ROUNDED)
            )
            return

        console.print(
            Panel(
                f"[bold cyan]Update Event: {
                    event.event_name}[/bold cyan]",
                box=box.ROUNDED,
                style="bold green",
            )
        )
        console.print(
            "[bold yellow](Leave blank to keep the current value.)[/bold yellow]\n"
        )

        event.event_name = Prompt.ask(
            "[bold yellow]Event name[/bold yellow]", default=event.event_name
        )
        event.event_start_date = parse_date(
            Prompt.ask(
                "[bold yellow]Start date (DD-MM-YYYY HH:MM)[/bold yellow]",
                default=event.event_start_date.strftime("%d-%m-%Y %H:%M"),
            ),
            event.event_start_date,
        )
        event.event_end_date = parse_date(
            Prompt.ask(
                "[bold yellow]End date (DD-MM-YYYY HH:MM)[/bold yellow]",
                default=event.event_end_date.strftime("%d-%m-%Y %H:%M"),
            ),
            event.event_end_date,
        )
        event.location = Prompt.ask(
            "[bold yellow]Location[/bold yellow]", default=event.location
        )
        attendees_input = Prompt.ask(
            "[bold yellow]Number of attendees[/bold yellow]",
            default=str(event.attendees),
        )

        try:
            event.attendees = int(attendees_input)
        except ValueError:
            console.print(
                Panel(
                    "[bold red]Invalid number of attendees.[/bold red]", box=box.ROUNDED
                )
            )
            return

        event.notes = Prompt.ask(
            "[bold yellow]Notes[/bold yellow]", default=event.notes
        )

        db.commit()
        console.print(
            Panel(
                "[bold green]Event updated successfully![/bold green]", box=box.ROUNDED
            )
        )
        sentry_sdk.capture_message(
            f"Event '{event.event_name}' updated successfully!", level="info"
        )

    except Exception as e:
        db.rollback()
        console.print(
            Panel(
                f"[bold red]Unexpected error: {
                    e}[/bold red]",
                box=box.ROUNDED,
            )
        )
        sentry_sdk.capture_exception(e)
    finally:
        db.close()
