ROLE_PERMISSIONS = {
    'Commercial': {
        'create_client', 'update_client', 'modify_contract',
        'filter_contracts', 'create_event', 'read_only', 'read_clients', 'read_contracts', 'read_events'
    },
    'Management': {
        'manage_users', 'create_contract', 'modify_contract', 'filter_events',
        'assign_support', 'read_only', 'read_clients', 'read_contracts', 'read_events'
    },
    'Support': {
        'filter_events', 'update_event', 'read_only', 'read_clients', 'read_contracts', 'read_events'
    }
}


def has_permission(employee, permission_name):
    """
    Checks if an employee has a specific permission.
    """
    role_name = employee.department.value
    return permission_name in ROLE_PERMISSIONS.get(role_name, set())
