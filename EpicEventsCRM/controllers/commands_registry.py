from rich.console import Console


console = Console()

# Basic commands and their descriptions
COMMANDS = {
    "menu": "Display the interactive menu.",
    "login": "Log in to the system.",
    "logout": "Log out of the system.",
    "status": "Display the current login status.",
    "list-clients": "List all clients.",
    "list-contracts": "List all contracts.",
    "list-events": "List all events.",
    "create-client": "Create a new client.",
    "update-client <client_id>": "Update an existing client.",
    "create-contract": "Create a new contract.",
    "update-contract <contract_id>": "Update an existing contract.",
    "create-event": "Create a new event.",
    "update-event <event_id>": "Update an existing event.",

    "create-employee": "Create a new employee.",
    "update-employee <employee_id>": "Update an existing employee.",
    "delete-employee <employee_id>": "Delete an employee.",
    "list-employees": "List all employees.",

}


def get_command_list():
    """
    Return the dictionary containing all basic commands and their descriptions.
    """
    return COMMANDS
