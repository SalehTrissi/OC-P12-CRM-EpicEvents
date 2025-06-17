# EpicEventsCRM - Commands Registry
COMMANDS = {
    # --- System & Interaction ---
    "status":                       "Display the current login status.",
    "menu":                         "Display the interactive menu.",
    "login":                        "Log in to the system.",

    # --- Employee Administration (Management Role) ---
    "create-employee":              "Create a new employee.",
    "update-employee <employee_id>": "Update an existing employee.",
    "delete-employee <employee_id>": "Delete an employee.",
    "list-employees":               "List all employees.",

    # --- Client Management ---
    "create-client":                "Create a new client.",
    "update-client <client_id>":    "Update an existing client.",
    "list-clients":                 "List all clients.",

    # --- Contract Management ---
    "create-contract":              "Create a new contract.",
    "update-contract <contract_id>": "Update an existing contract.",
    "list-contracts":               "List all contracts.",

    # --- Event Management ---
    "create-event":                 "Create a new event.",
    "update-event <event_id>":      "Update an existing event.",
    "list-events":                  "List all events.",

    # --- Session Finalization ---
    "logout":                       "Log out of the system.",
}


def get_command_list():
    """
    Return the dictionary containing all basic commands and their descriptions.
    """
    return COMMANDS
