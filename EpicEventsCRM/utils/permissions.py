# File: EpicEventsCRM/utils/permissions.py (Refactored)

from EpicEventsCRM.controllers.commands_registry import get_command_list
from EpicEventsCRM.models.employee_model import Employee


ROLE_PERMISSIONS = {
    "Commercial": {
        "create_client",
        "update_client",
        "update_contract",
        "create_event",
        "list_clients",
        "list_contracts",
        "list_events",
    },
    "Management": {
        "create_employee",
        "update_employee",
        "delete_employee",
        "list_employees",
        "create_contract",
        "update_contract",
        "update_event",
        "assign_support",
        "list_clients",
        "list_contracts",
        "list_events",
    },
    "Support": {
        "update_event",
        "list_clients",
        "list_contracts",
        "list_events",
    },
}


def has_permission(employee: Employee, permission_name: str) -> bool:
    """
    Checks if an employee's role grants them a specific permission.

    Args:
        employee: The employee object to check.
        permission_name: The name of the permission string.

    Returns:
        True if the employee has the permission, False otherwise.
    """
    role_name = employee.department.value
    return permission_name in ROLE_PERMISSIONS.get(role_name, set())


def get_available_commands(employee: Employee) -> list:
    """
    Returns a list of commands available to the employee based on their role.

    Args:
        employee: The currently logged-in employee object.

    Returns:
        A list of (command_name, description) tuples for available commands.
    """
    commands = get_command_list()
    always_available = {"menu", "logout", "status"}

    available_commands = []
    for command, description in commands.items():
        base_command = command.split(" ")[0]
        normalized_command = base_command.replace("-", "_")

        # Check if the command is always available or if the user has permission
        if base_command in always_available or has_permission(employee, normalized_command):
            available_commands.append((command, description))

    return available_commands
