from EpicEventsCRM.utils.validators import (
    validate_email,
    validate_phone_number,
    validate_string_length,
)
from EpicEventsCRM.utils.permissions import has_permission
from EpicEventsCRM.models.client_model import Client
from sqlalchemy.exc import IntegrityError
from db.database import get_db
from auth import get_current_user
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from rich import box
import sentry_sdk


console = Console()


def create_client():
    """Creates a new client interactively with validation and database integration."""
    current_user = get_current_user()

    if not current_user:
        console.print(
            Panel("[bold red]Authentication required.[/bold red]", box=box.ROUNDED)
        )
        return

    if not has_permission(current_user, "create_client"):
        console.print(
            Panel("[bold red]Insufficient permissions.[/bold red]", box=box.ROUNDED)
        )
        return

    console.print(
        Panel(
            "[bold cyan]Create New Client[/bold cyan]",
            box=box.ROUNDED,
            style="bold green",
        )
    )

    db = next(get_db())

    # Collecting client information with validation
    full_name = Prompt.ask("[bold yellow]Enter full name[/bold yellow]")
    validate_string_length(full_name, "Full name", 100)

    while True:
        email = Prompt.ask("[bold yellow]Enter email address[/bold yellow]")
        try:
            validate_email(email)
            break
        except ValueError as e:
            console.print(Panel(f"[bold red]{e}[/bold red]", box=box.ROUNDED))

    while True:
        phone_number = Prompt.ask("[bold yellow]Enter phone number[/bold yellow]")
        try:
            validate_phone_number(phone_number)
            break
        except ValueError as e:
            console.print(Panel(f"[bold red]{e}[/bold red]", box=box.ROUNDED))

    company_name = Prompt.ask("[bold yellow]Enter company name[/bold yellow]")
    validate_string_length(company_name, "Company name", 100)

    client = Client(
        full_name=full_name,
        email=email,
        phone_number=phone_number,
        company_name=company_name,
        sales_contact=current_user,
    )

    # Save to database
    try:
        db.add(client)
        db.commit()
        console.print(
            Panel(
                f"[bold green]Client '{
                    full_name}' created successfully![/bold green]",
                box=box.ROUNDED,
            )
        )
        sentry_sdk.capture_message(
            f"Client '{full_name}' created successfully!", level="info"
        )
    except IntegrityError:
        db.rollback()
        console.print(
            Panel(
                "[bold red]Error: A client with this email already exists.[/bold red]",
                box=box.ROUNDED,
            )
        )
        sentry_sdk.capture_exception(IntegrityError("Duplicate email"))
    except Exception as e:
        db.rollback()
        console.print(
            Panel(
                f"[bold red]Error creating client: {
                    e}[/bold red]",
                box=box.ROUNDED,
            )
        )
        sentry_sdk.capture_exception(e)
    finally:
        db.close()


def update_client(client_id):
    """Updates a client's information interactively with validation
    and error handling."""
    current_user = get_current_user()

    if not current_user:
        console.print(
            Panel("[bold red]Authentication required.[/bold red]", box=box.ROUNDED)
        )
        return

    db = next(get_db())

    client = db.query(Client).filter_by(client_id=client_id).first()
    if not client:
        console.print(Panel("[bold red]Client not found.[/bold red]", box=box.ROUNDED))
        return

    if not has_permission(current_user, "update_client"):
        console.print(
            Panel(
                "[bold red]You do not have permission to update this client."
                "[/bold red]",
                box=box.ROUNDED,
            ))
        return

    console.print(
        Panel(
            f"[bold cyan]Update Client: {
                client.full_name}[/bold cyan]",
            box=box.ROUNDED,
            style="bold green",
        )
    )
    console.print(
        "[bold yellow](Leave blank to keep the current value.)[/bold yellow]\n"
    )

    # Collecting new information
    full_name = Prompt.ask(
        "[bold yellow]Full name[/bold yellow]", default=client.full_name
    )
    validate_string_length(full_name, "Full name", 100)

    while True:
        email = Prompt.ask("[bold yellow]Email[/bold yellow]", default=client.email)
        try:
            validate_email(email)
            break
        except ValueError as e:
            console.print(Panel(f"[bold red]{e}[/bold red]", box=box.ROUNDED))

    while True:
        phone_number = Prompt.ask(
            "[bold yellow]Phone number[/bold yellow]", default=client.phone_number
        )
        try:
            validate_phone_number(phone_number)
            break
        except ValueError as e:
            console.print(Panel(f"[bold red]{e}[/bold red]", box=box.ROUNDED))

    company_name = Prompt.ask(
        "[bold yellow]Company name[/bold yellow]", default=client.company_name
    )
    validate_string_length(company_name, "Company name", 100)

    # Update client details
    client.full_name = full_name
    client.email = email
    client.phone_number = phone_number
    client.company_name = company_name

    # Save changes to database
    try:
        db.commit()
        console.print(
            Panel(
                f"[bold green]Client '{
                    full_name}' updated successfully![/bold green]",
                box=box.ROUNDED,
            )
        )
        sentry_sdk.capture_message(
            f"Client '{full_name}' updated successfully!", level="info"
        )
    except IntegrityError:
        db.rollback()
        console.print(
            Panel(
                "[bold red]Error: A client with this email already exists.[/bold red]",
                box=box.ROUNDED,
            )
        )
        sentry_sdk.capture_exception(IntegrityError("Duplicate email"))
    except Exception as e:
        db.rollback()
        console.print(
            Panel(
                f"[bold red]Error updating client: {
                    e}[/bold red]",
                box=box.ROUNDED,
            )
        )
        sentry_sdk.capture_exception(e)
    finally:
        db.close()
