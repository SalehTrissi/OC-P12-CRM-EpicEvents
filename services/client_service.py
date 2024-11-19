from EpicEventsCRM.utils.permissions import has_permission
from EpicEventsCRM.models.client_model import Client
from sqlalchemy.exc import IntegrityError
from db.database import SessionLocal
from auth import get_current_user
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from rich import box


console = Console()


def create_client():
    """
    Creates a new client with a user-friendly and visually appealing interface.
    """
    current_user = get_current_user()
    if not current_user:
        console.print(
            Panel("[bold red]You must be authenticated to create a client.[/bold red]", box=box.ROUNDED))
        return

    if not has_permission(current_user, 'create_client'):
        console.print(
            Panel("[bold red]You do not have permission to create a client.[/bold red]", box=box.ROUNDED))
        return

    console.print(Panel("[bold cyan]Create New Client[/bold cyan]",
                        box=box.ROUNDED, style="bold green"))

    # Collecting client information
    full_name = Prompt.ask("[bold yellow]Enter full name[/bold yellow]")
    email = Prompt.ask("[bold yellow]Enter email address[/bold yellow]")
    phone_number = Prompt.ask("[bold yellow]Enter phone number[/bold yellow]")
    company_name = Prompt.ask("[bold yellow]Enter company name[/bold yellow]")

    client = Client(
        full_name=full_name,
        email=email,
        phone_number=phone_number,
        company_name=company_name,
        sales_contact=current_user
    )

    # Save to database
    with SessionLocal as session:
        session.add(client)
        try:
            session.commit()
            console.print(
                Panel(f"[bold green]Client '{full_name}' created successfully![/bold green]",
                      box=box.ROUNDED))
        except IntegrityError:
            session.rollback()
            console.print(Panel(
                "[bold red]Error: A client with this email already exists.[/bold red]", box=box.ROUNDED))
        except Exception as e:
            session.rollback()
            console.print(Panel(f"[bold red]Error creating client: {
                          e}[/bold red]", box=box.ROUNDED))


def update_client(client_id):
    """
    Updates a client's information with a user-friendly and visually appealing interface.
    """
    current_user = get_current_user()
    if not current_user:
        console.print(
            Panel("[bold red]You must be authenticated to update a client.[/bold red]", box=box.ROUNDED))
        return

    with SessionLocal as session:
        client = session.query(Client).filter_by(client_id=client_id).first()
        if not client:
            console.print(
                Panel("[bold red]Client not found.[/bold red]", box=box.ROUNDED))
            return

        if not has_permission(current_user, 'update_client'):
            console.print(
                Panel("[bold red]You do not have permission to update this client.[/bold red]", box=box.ROUNDED))
            return

        console.print(Panel(f"[bold cyan]Update Client: {client.full_name}[/bold cyan]",
                            box=box.ROUNDED, style="bold green"))

        console.print(
            "[bold yellow](Leave blank to keep the current value.)[/bold yellow]\n")

        # Collecting new information
        full_name = Prompt.ask(
            f"[bold yellow]Full name[/bold yellow] [bold green](current: {
                client.full_name})[/bold green]",
            default=client.full_name,
            show_default=False
        )
        email = Prompt.ask(
            f"[bold yellow]Email[/bold yellow] [bold green](current: {
                client.email})[/bold green]",
            default=client.email,
            show_default=False
        )
        phone_number = Prompt.ask(
            f"[bold yellow]Phone number[/bold yellow] [bold green](current: {
                client.phone_number})[/bold green]",
            default=client.phone_number,
            show_default=False
        )
        company_name = Prompt.ask(
            f"[bold yellow]Company name[/bold yellow] [bold green](current: {
                client.company_name})[/bold green]",
            default=client.company_name,
            show_default=False
        )

        # Update client details
        client.full_name = full_name
        client.email = email
        client.phone_number = phone_number
        client.company_name = company_name

        # Save changes to database
        try:
            session.commit()
            console.print(
                Panel(f"[bold green]Client '{full_name}' updated successfully![/bold green]",
                      box=box.ROUNDED))
        except IntegrityError:
            session.rollback()
            console.print(Panel(
                "[bold red]Error: A client with this email already exists.[/bold red]", box=box.ROUNDED))
        except Exception as e:
            session.rollback()
            console.print(Panel(f"[bold red]Error updating client: {
                          e}[/bold red]", box=box.ROUNDED))
