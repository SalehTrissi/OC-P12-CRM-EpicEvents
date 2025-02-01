from EpicEventsCRM.controllers.commands_registry import get_command_list


ROLE_PERMISSIONS = {
    "Commercial": {
        "create_client",
        "update_client",
        "modify_contract",
        "filter_contracts",
        "create_event",
        "read_only",
        "list_clients",
        "list_contracts",
        "list_events",
    },
    "Management": {
        "manage_users",
        "create_contract",
        "modify_contract",
        "filter_events",
        "assign_support",
        "read_only",
        "list_clients",
        "list_contracts",
        "list_events",
    },
    "Support": {
        "filter_events",
        "update_event",
        "read_only",
        "list_clients",
        "list_contracts",
        "list_events",
    },
}


def has_permission(employee, permission_name):
    """
    Check if an employee has a specific permission.
    :param employee: The current employee object.
    :param permission_name: The permission name to check.
    :return: True or False
    """
    role_name = employee.department.value
    return permission_name in ROLE_PERMISSIONS.get(role_name, set())


def get_available_commands(employee):
    """
    Return a list of commands available to the currently logged-in employee,
    based on their role permissions.
    :param employee: The current employee object.
    :return: A list of tuples (command_name, description) for the available commands.
    """
    commands = get_command_list()

    # These commands are always available
    always_available = {
        "menu",
        "logout",
        "status",
        "list-clients",
        "list-contracts",
        "list-events",
    }

    available_commands = []
    for command, description in commands.items():
        normalized_command = command.replace("-", "_")
        # If command is in always_available or in the employee's role permissions
        if command in always_available or normalized_command in ROLE_PERMISSIONS.get(
            employee.department.value, {}
        ):
            available_commands.append((command, description))

    return available_commands
