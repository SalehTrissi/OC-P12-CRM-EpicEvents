from services.data_access import get_all_clients, get_all_contracts, get_all_events


def list_clients():
    """
    Lists all clients with proper error handling.
    """
    try:
        clients = get_all_clients()
        if not clients:
            print("No clients found in the database.")
        else:
            for client in clients:
                print(f"Client ID: {client.client_id}, Name: {
                      client.full_name}, Email: {client.email}")
    except PermissionError as e:
        print(e)


def list_contracts():
    """
    Lists all contracts with proper error handling.
    """
    try:
        contracts = get_all_contracts()
        if not contracts:
            print("No contracts found in the database.")
        else:
            for contract in contracts:
                print(f"Contract ID: {contract.contract_id}, Total amount: {
                      contract.total_amount}, Remaining amount: {
                      contract.remaining_amount}, Signed: {contract.is_signed}")
    except PermissionError as e:
        print(e)


def list_events():
    """
    Lists all events with proper error handling.
    """
    try:
        events = get_all_events()
        if not events:
            print("No events found in the database.")
        else:
            for event in events:
                print(f"Event ID: {event.event_id}, Name: {
                      event.event_name}, Start Date: {event.event_start_date}")
    except PermissionError as e:
        print(e)
