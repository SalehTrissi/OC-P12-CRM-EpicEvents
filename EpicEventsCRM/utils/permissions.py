# Defining permissions for each role
ROLE_PERMISSIONS = {
    'Commercial': {
        'create_client', 'update_client', 'modify_contract',
        'filter_contracts', 'create_event', 'read_only'
    },
    'Management': {
        'manage_users', 'create_modify_contract', 'filter_events',
        'assign_support', 'read_only'
    },
    'Support': {
        'filter_events', 'update_event', 'read_only'
    }
}


def has_permission(employee, permission_name):
    """
    Checks if an employee has a specific permission.
    """
    role_name = employee.department.value
    return permission_name in ROLE_PERMISSIONS.get(role_name, set())
