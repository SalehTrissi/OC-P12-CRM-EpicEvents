from services.data_access import get_all_clients, get_all_contracts, get_all_events
from rich.console import Console
from rich.table import Table
from rich import box


console = Console()


def list_clients():
    """
    Lists all clients with proper error handling and displays them in a detailed table.
    """
    try:
        clients = get_all_clients()
        if not clients:
            console.print(
                "[bold yellow]No clients found in the database.[/bold yellow]"
            )
        else:
            table = Table(
                title="[bold cyan]Client List[/bold cyan]",
                title_style="bold magenta",
                box=box.ROUNDED,
                header_style="bold white",
                show_lines=True,
            )
            table.add_column("Client ID", justify="center", style="cyan", no_wrap=True)
            table.add_column("Full Name", justify="center", style="green")
            table.add_column("Email", justify="center", style="magenta")
            table.add_column("Phone Number", justify="center", style="yellow")
            table.add_column("Company Name", justify="center", style="blue")
            table.add_column("Created Date", justify="center", style="cyan")
            table.add_column("Last Contact Date", justify="center", style="cyan")
            table.add_column("Sales Contact", justify="center", style="green")

            for client in clients:
                table.add_row(
                    str(client.client_id),
                    client.full_name,
                    client.email,
                    client.phone_number,
                    client.company_name,
                    client.date_created.strftime("%d-%m-%Y %H:%M:%S"),
                    client.last_contact_date.strftime("%d-%m-%Y %H:%M:%S"),
                    f"{client.sales_contact.first_name} {
                        client.sales_contact.last_name}",
                )

            console.print(table)
    except PermissionError as e:
        console.print(f"[bold red]{e}[/bold red]")


def list_contracts():
    """
    Lists all contracts with proper error handling and
    displays them in a detailed table.
    """
    try:
        contracts = get_all_contracts()
        if not contracts:
            console.print(
                "[bold yellow]No contracts found in the database.[/bold yellow]"
            )
        else:
            table = Table(
                title="[bold cyan]Contract List[/bold cyan]",
                title_style="bold magenta",
                box=box.ROUNDED,
                header_style="bold white",
                show_lines=True,
            )
            table.add_column(
                "Contract ID", justify="center", style="cyan", no_wrap=True
            )
            table.add_column("Client", justify="left", style="cyan")
            table.add_column("Client Contacts", justify="center", style="magenta")
            table.add_column("Total Amount", justify="right", style="green")
            table.add_column("Remaining Amount", justify="right", style="yellow")
            table.add_column("Status", justify="center", style="magenta")
            table.add_column("Created Date", justify="center", style="blue")

            table.add_column("Sales Contact", justify="left", style="green")

            for contract in contracts:
                table.add_row(
                    str(contract.contract_id),
                    contract.client.full_name,
                    f"{contract.client.email} \n {contract.client.phone_number}",
                    f"{contract.total_amount:.2f}€",
                    f"{contract.remaining_amount:.2f}€",
                    (
                        "[bold green]Signed[/bold green]"
                        if contract.is_signed
                        else "[bold red]Unsigned[/bold red]"
                    ),
                    contract.date_created.strftime("%d-%m-%Y %H:%M:%S"),
                    f"{contract.sales_contact.first_name} {
                        contract.sales_contact.last_name}",
                )

            console.print(table)
    except PermissionError as e:
        console.print(f"[bold red]{e}[/bold red]")


def list_events():
    """
    Lists all events with proper error handling and displays them in a detailed table.
    """
    try:
        events = get_all_events()
        if not events:
            console.print("[bold yellow]No events found in the database.[/bold yellow]")
        else:
            table = Table(
                title="[bold cyan]Event List[/bold cyan]",
                title_style="bold magenta",
                box=box.ROUNDED,
                header_style="bold white",
                show_lines=True,
            )
            table.add_column("Event ID", justify="center", style="cyan", no_wrap=True)
            table.add_column(
                "Contract ID", justify="center", style="cyan", no_wrap=True
            )
            table.add_column("Event Name", justify="center", style="green")
            table.add_column("Client Name", justify="center", style="green")
            table.add_column("Client Contacts", justify="center", style="magenta")
            table.add_column("Start Date", justify="center", style="green")
            table.add_column("End Date", justify="center", style="red")
            table.add_column("Location", justify="center", style="yellow")
            table.add_column("Attendees", justify="center", style="cyan")
            table.add_column("Support Contact", justify="center", style="cyan")
            table.add_column("Notes", justify="center", style="magenta")

            for event in events:
                table.add_row(
                    str(event.event_id),
                    str(event.contract_id),
                    event.event_name,
                    event.client.full_name,
                    f"{event.client.email} \n {event.client.phone_number}",
                    event.event_start_date.strftime("%d-%m-%Y %H:%M:%S"),
                    event.event_end_date.strftime("%d-%m-%Y %H:%M:%S"),
                    event.location,
                    str(event.attendees),
                    f"{event.support_contact.first_name} {
                        event.support_contact.last_name}",
                    event.notes,
                )

            console.print(table)
    except PermissionError as e:
        console.print(f"[bold red]{e}[/bold red]")
