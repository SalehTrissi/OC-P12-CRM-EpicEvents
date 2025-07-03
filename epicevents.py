import click
import sys
from auth import login as auth_login, logout as auth_logout, status as auth_status
from services.list_services import list_clients, list_contracts, list_events, list_employees
from services.employee_service import create_employee, update_employee, delete_employee
from services.contract_service import create_contract, update_contract
from services.client_service import create_client, update_client
from services.event_service import create_event, update_event
from EpicEventsCRM.controllers.general_commands import help_command
from EpicEventsCRM.controllers.menus import run_menu_loop


@click.group()
def cli():
    """Epic Events CRM Command Line Interface."""
    pass


@cli.command(name="menu")
def menu_command():
    """Starts the interactive menu loop."""
    run_menu_loop(cli)


# --- All other command definitions remain unchanged ---
@cli.command(name="login")
def login_command():
    auth_login()
    # After login, automatically start the menu
    run_menu_loop(cli)


@cli.command(name="logout")
def logout_command():
    auth_logout()


@cli.command(name="status")
def status_command():
    auth_status()


@cli.command(name="list-clients")
def list_clients_command():
    list_clients()


@cli.command(name="list-contracts")
@click.option('--not-signed', is_flag=True, help="Display unsigned contracts.")
@click.option('--not-paid', is_flag=True, help="Display contracts that are not fully paid.")
def list_contracts_command(not_signed, not_paid):
    """Lists contracts with optional filters."""
    list_contracts(not_signed=not_signed, not_paid=not_paid)


@cli.command(name="list-events")
@click.option('--no-support', is_flag=True, help="Display events with no support contact assigned.")
@click.option('--my-events', is_flag=True, help="Display only your assigned events (for Support staff).")
def list_events_command(no_support, my_events):
    """Lists events with optional filters."""
    list_events(no_support=no_support, my_events=my_events)


@cli.command(name="list-employees")
def list_employees_command():
    list_employees()


@cli.command(name="create-employee")
def create_employee_command():
    create_employee()


@cli.command(name="update-employee")
@click.argument("employee_id", type=int)
def update_employee_command(employee_id):
    update_employee(employee_id)


@cli.command(name="delete-employee")
@click.argument("employee_id", type=int)
def delete_employee_command(employee_id):
    delete_employee(employee_id)


@cli.command(name="create-client")
def create_client_command():
    create_client()


@cli.command(name="update-client")
@click.argument("client_id", type=int)
def update_client_command(client_id):
    update_client(client_id)


@cli.command(name="create-contract")
def create_contract_command():
    create_contract()


@cli.command(name="update-contract")
@click.argument("contract_id", type=int)
def update_contract_command(contract_id):
    update_contract(contract_id)


@cli.command(name="create-event")
def create_event_command():
    create_event()


@cli.command(name="update-event")
@click.argument("event_id", type=int)
def update_event_command(event_id):
    update_event(event_id)


@cli.command(name="help")
def help_cli_command():
    help_command()


if __name__ == "__main__":
    # If the script is run without arguments, default to the menu
    if len(sys.argv) == 1:
        menu_command.main()
    else:
        cli()
