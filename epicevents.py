from services.data_access import get_all_clients, get_all_contracts, get_all_events
from services.employee_service import create_employee, update_employee
from services.contract_service import create_contract, update_contract
from services.client_service import create_client, update_client
from auth import login, logout, status
import argparse


def list_clients():
    clients = get_all_clients()
    if not clients:
        print("No clients found in the database.")
    else:
        for client in clients:
            print(f"Client ID: {client.client_id}, Name: {
                  client.full_name}, Email: {client.email}")


def list_contracts():
    contracts = get_all_contracts()
    if not contracts:
        print("No contracts found in the database.")
    else:
        for contract in contracts:
            print(f"Contract ID: {contract.contract_id}, Amount: {
                  contract.amount}, Signed: {contract.signed}")


def list_events():
    events = get_all_events()
    if not events:
        print("No events found in the database.")
    else:
        for event in events:
            print(f"Event ID: {event.event_id}, Name: {event.name}, Date: {event.date}")


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

    args = parser.parse_args()

    if args.command == 'login':
        login()
    elif args.command == 'logout':
        logout()
    elif args.command == 'status':
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
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
