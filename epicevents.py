import click
import argparse
from services.list_services import list_clients, list_contracts, list_events
from services.employee_service import create_employee, update_employee
from services.contract_service import create_contract, update_contract
from services.client_service import create_client, update_client
from services.event_service import create_event, update_event
from auth import login as auth_login, logout as auth_logout, status


@click.group()
def cli():
    """Epic Events CRM"""
    pass


@cli.command(name="login")
def login_command():
    """Log in"""
    auth_login()


@cli.command(name="logout")
def logout_command():
    """Log out"""
    auth_logout()


if __name__ == "__main__":
    cli()


def main():
    parser = argparse.ArgumentParser(description="Epic Events CRM")
    subparsers = parser.add_subparsers(dest='command')

    # Command login
    subparsers.add_parser('login', help='Se connecter')

    # Command logout
    subparsers.add_parser('logout', help='Se déconnecter')

    # Command status
    subparsers.add_parser('status', help='Afficher le statut de connexion')

    # Command list_clients
    subparsers.add_parser('list_clients', help='List all clients')

    # Command list_contracts
    subparsers.add_parser('list_contracts', help='List all contracts')

    # Command list_events
    subparsers.add_parser('list_events', help='List all events')

    # create_employee command
    subparsers.add_parser('create_employee', help='Create a new employee')

    # update_employee command
    parser_update_employee = subparsers.add_parser(
        'update_employee', help='Update an employee')
    parser_update_employee.add_argument(
        'employee_id', type=int, help='ID of the employee to update')

    # create_client command
    subparsers.add_parser('create_client', help='Create a new client')

    # update_client command
    parser_update_client = subparsers.add_parser(
        'update_client', help='Update an client')
    parser_update_client.add_argument(
        'client_id', type=int, help='ID of the client to update')

    # create_contract command
    subparsers.add_parser('create_contract', help='Create a new contract')

    # Command update_contract
    parser_update_contract = subparsers.add_parser(
        'update_contract', help='Update a contract')
    parser_update_contract.add_argument(
        'contract_id', type=int, help='ID of the contract to update')

    # create_event command
    subparsers.add_parser('create_event', help='Create a new event')

    # update_event command
    parser_update_event = subparsers.add_parser('update_event', help='Update an event')
    parser_update_event.add_argument(
        'event_id', type=int, help='ID of the event to update')

    args = parser.parse_args()

    if args.command == 'status':
        status()
    elif args.command == 'list_clients':
        list_clients()
    elif args.command == 'list_contracts':
        list_contracts()
    elif args.command == 'list_events':
        list_events()
    elif args.command == 'create_employee':
        create_employee()
    elif args.command == 'update_employee':
        update_employee(args.employee_id)
    elif args.command == 'create_client':
        create_client()
    elif args.command == 'update_client':
        update_client(args.client_id)
    elif args.command == 'create_contract':
        create_contract()
    elif args.command == 'update_contract':
        update_contract(args.contract_id)
    elif args.command == 'create_event':
        create_event()
    elif args.command == 'update_event':
        update_event(args.event_id)
    else:
        parser.print_help()
