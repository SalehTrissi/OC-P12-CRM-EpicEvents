import os
import click
from rich.console import Console
from auth import login as auth_login, logout as auth_logout, status as auth_status
from services.list_services import list_clients, list_contracts, list_events
from services.employee_service import create_employee, update_employee
from services.contract_service import create_contract, update_contract
from services.client_service import create_client, update_client
from services.event_service import create_event, update_event
from EpicEventsCRM.controllers.general_commands import help_command
from EpicEventsCRM.controllers.menus import display_menu

console = Console()


@click.group()
def cli():
    """Epic Events CRM Command Line Interface."""
    pass


@cli.command(name="menu")
def menu_command():
    """
    Display an interactive menu of available commands.
    This will keep displaying the menu until the user chooses to exit (0).
    """
    while True:
        # Show the menu and get the chosen command
        command = display_menu()

        # If command is None, user chose 0 => exit
        if command is None:
            console.print("[bold red]👋 Exiting menu... Goodbye![/bold red]")
            return

        # Execute the command unless it's "menu" (just redisplay the menu)
        if command != "menu":
            try:
                cli.main(args=[command], standalone_mode=False)

                if command not in ["logout", "exit"]:
                    console.input(
                        "\n[bold cyan]Press ENTER to return to the menu...[/bold cyan]")

            except Exception as e:
                console.print(f"[bold red]Error executing command: {str(e)}[/bold red]")


@cli.command(name="login")
def login_command():
    """Log in to the system."""
    auth_login()
    cli.main(args=["menu"], standalone_mode=False)


@cli.command(name="logout")
def logout_command():
    """Log out of the system."""
    auth_logout()

    # Clear the screen before displaying the logout message
    os.system("cls" if os.name == "nt" else "clear")

    console.print("[bold cyan]You have been logged out successfully.[/bold cyan]")

    # Instead of directly calling menu, exit completely
    return


@cli.command(name="status")
def status_command():
    """Show the current login status."""
    auth_status()


@cli.command(name="list-clients")
def list_clients_command():
    """List all clients."""
    list_clients()


@cli.command(name="list-contracts")
def list_contracts_command():
    """List all contracts."""
    list_contracts()


@cli.command(name="list-events")
def list_events_command():
    """List all events."""
    list_events()


@cli.command(name="create-employee")
def create_employee_command():
    """Create a new employee."""
    create_employee()


@cli.command(name="update-employee")
@click.argument("employee_id", type=int)
def update_employee_command(employee_id):
    """Update an existing employee."""
    update_employee(employee_id)


@cli.command(name="create-client")
def create_client_command():
    """Create a new client."""
    create_client()


@cli.command(name="update-client")
@click.argument("client_id", type=int)
def update_client_command(client_id):
    """Update an existing client."""
    update_client(client_id)


@cli.command(name="create-contract")
def create_contract_command():
    """Create a new contract."""
    create_contract()


@cli.command(name="update-contract")
@click.argument("contract_id", type=int)
def update_contract_command(contract_id):
    """Update an existing contract."""
    update_contract(contract_id)


@cli.command(name="create-event")
def create_event_command():
    """Create a new event."""
    create_event()


@cli.command(name="update-event")
@click.argument("event_id", type=int)
def update_event_command(event_id):
    """Update an existing event."""
    update_event(event_id)


@cli.command(name="help")
def help_cli_command():
    """Show help for all commands."""
    help_command()


if __name__ == "__main__":
    cli()
