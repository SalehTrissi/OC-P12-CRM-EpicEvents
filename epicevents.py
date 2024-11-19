from auth import login as auth_login, logout as auth_logout, status as auth_status
from services.list_services import list_clients, list_contracts, list_events
from services.employee_service import create_employee, update_employee
from services.contract_service import create_contract, update_contract
from services.client_service import create_client, update_client
from services.event_service import create_event, update_event
import argparse
import click


@click.group()
def cli():
    """Epic Events CRM"""
    pass


@cli.command(name="login")
def login_command():
    """Command log in"""
    auth_login()


@cli.command(name="logout")
def logout_command():
    """Command log out"""
    auth_logout()


@cli.command(name="status")
def status_command():
    """Command status"""
    auth_status()


@cli.command(name="list-clients")
def list_clients_command():
    """Command to list all clients"""
    list_clients()


@cli.command(name="list-contracts")
def list_contracts_command():
    """Command to list all contracts"""
    list_contracts()


@cli.command(name="list-events")
def list_events_command():
    """Command to list all events"""
    list_events()


@cli.command(name="create-employee")
def create_employee_command():
    """Create a new employee"""
    create_employee()


@cli.command(name="update-employee")
@click.argument("employee_id", type=int)
def update_employee_command(employee_id):
    """Update an existing employee"""
    update_employee(employee_id)


@cli.command(name="create-client")
def create_client_command():
    """Create a new client"""
    create_client()


@cli.command(name="update-client")
@click.argument("client_id", type=int)
def update_client_command(client_id):
    """Update an existing client"""
    update_client(client_id)


@cli.command(name="create-contract")
def create_contract_command():
    """Create a new contract"""
    create_contract()


@cli.command(name="update-contract")
@click.argument("contract_id", type=int)
def update_contract_command(contract_id):
    """Update an existing contract"""
    update_contract(contract_id)


if __name__ == "__main__":
    cli()


def main():
    parser = argparse.ArgumentParser(description="Epic Events CRM")
    subparsers = parser.add_subparsers(dest='command')

    # create_event command
    subparsers.add_parser('create_event', help='Create a new event')

    # update_event command
    parser_update_event = subparsers.add_parser('update_event', help='Update an event')
    parser_update_event.add_argument(
        'event_id', type=int, help='ID of the event to update')

    args = parser.parse_args()

    if args.command == 'create_event':
        create_event()
    elif args.command == 'update_event':
        update_event(args.event_id)
    else:
        parser.print_help()
