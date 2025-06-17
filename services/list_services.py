from services.data_access import get_all_clients, get_all_contracts, get_all_events, get_all_employees
from rich.console import Console
from rich.table import Table
from rich import box


console = Console()


def _display_table(title: str, get_data_func, column_configs: list, row_formatter_func):
    """
    Generic function to display a data table.
    It handles data retrieval, no-data cases, table creation,
    and the display of formatted rows.
    """
    try:
        items = get_data_func()
        if not items:
            console.print(
                f"[bold yellow]No {title.lower()} found in the database.[/bold yellow]")
            return

        table = Table(
            title=f"[bold cyan]{title}[/bold cyan]",
            box=box.ROUNDED,
            header_style="bold white",
            show_lines=True,
        )

        for col_config in column_configs:
            table.add_column(**col_config)

        for item in items:
            table.add_row(*row_formatter_func(item))

        console.print(table)
    except PermissionError as e:
        console.print(f"[bold red]{e}[/bold red]")


# --- Specific Configurations and Formatters ---

# Configuration for the clients table
CLIENT_COLUMNS = [
    {"header": "Client ID", "justify": "center", "style": "cyan", "no_wrap": True},
    {"header": "Full Name", "style": "green"},
    {"header": "Email", "style": "magenta"},
    {"header": "Phone Number", "style": "yellow"},
    {"header": "Company Name", "style": "blue"},
    {"header": "Created Date", "justify": "center", "style": "cyan"},
    {"header": "Last Contact", "justify": "center", "style": "cyan"},
    {"header": "Sales Contact", "style": "green"},
]


def _format_client_row(client):
    """Formats a row for the clients table."""
    sales_contact = client.sales_contact
    contact_name = f"{sales_contact.first_name} {sales_contact.last_name}" if sales_contact else "N/A"
    return (
        str(client.client_id),
        client.full_name,
        client.email,
        client.phone_number,
        client.company_name,
        client.date_created.strftime("%d-%m-%Y"),
        client.last_contact_date.strftime("%d-%m-%Y"),
        contact_name,
    )


# Configuration for the contracts table
CONTRACT_COLUMNS = [
    {"header": "Contract ID", "justify": "center", "style": "cyan", "no_wrap": True},
    {"header": "Client", "style": "cyan"},
    {"header": "Total Amount", "justify": "right", "style": "green"},
    {"header": "Remaining", "justify": "right", "style": "yellow"},
    {"header": "Status", "justify": "center", "style": "magenta"},
    {"header": "Sales Contact", "style": "green"},
]


def _format_contract_row(contract):
    """Formats a row for the contracts table."""
    status = "[bold green]Signed[/bold green]" if contract.is_signed else "[bold red]Unsigned[/bold red]"
    sales_contact = contract.sales_contact
    contact_name = f"{sales_contact.first_name} {sales_contact.last_name}" if sales_contact else "N/A"
    return (
        str(contract.contract_id),
        contract.client.full_name,
        f"{contract.total_amount:.2f}€",
        f"{contract.remaining_amount:.2f}€",
        status,
        contact_name,
    )


# Configuration for the events table
EVENT_COLUMNS = [
    {"header": "Event ID", "justify": "center", "style": "cyan", "no_wrap": True},
    {"header": "Event Name", "style": "green"},
    {"header": "Client", "style": "cyan"},
    {"header": "Location", "style": "yellow"},
    {"header": "Attendees", "justify": "center", "style": "blue"},
    {"header": "Dates", "justify": "center"},
    {"header": "Support Contact", "style": "magenta"},
]


def _format_event_row(event):
    """Formats a row for the events table."""
    support_contact = event.support_contact
    contact_name = (
        f"{support_contact.first_name} {support_contact.last_name}"
        if support_contact else "[dim]Not Assigned[/dim]"
    )
    dates = (
        f"{event.event_start_date.strftime('%d-%m-%y %Hh%M')} - "
        f"{event.event_end_date.strftime('%d-%m-%y %Hh%M')}"
    )
    return (
        str(event.event_id),
        event.event_name,
        event.client.full_name,
        event.location,
        str(event.attendees),
        dates,
        contact_name,
    )


# Configuration for the employees table
EMPLOYEE_COLUMNS = [
    {"header": "Employee ID", "justify": "center", "style": "cyan", "no_wrap": True},
    {"header": "Full Name", "style": "green"},
    {"header": "Email", "style": "magenta"},
    {"header": "Phone Number", "style": "yellow"},
    {"header": "Department", "style": "blue"},
    {"header": "Role", "style": "cyan"},
]


def _format_employee_row(employee):
    """Formats a row for the employees table."""
    return (
        str(employee.employee_id),
        f"{employee.first_name} {employee.last_name}",
        employee.email,
        employee.phone_number,
        employee.department.value,
        employee.department.value,
    )

# --- Public Functions (Simple and Clean) ---


def list_clients():
    """Lists all clients by calling the generic display table function."""
    _display_table("Client List", get_all_clients, CLIENT_COLUMNS, _format_client_row)


def list_contracts():
    """Lists all contracts by calling the generic display table function."""
    _display_table("Contract List", get_all_contracts,
                   CONTRACT_COLUMNS, _format_contract_row)


def list_events():
    """Lists all events by calling the generic display table function."""
    _display_table("Event List", get_all_events, EVENT_COLUMNS, _format_event_row)


def list_employees():
    """Lists all employees by calling the generic display table function."""
    _display_table("Employee List", get_all_employees,
                   EMPLOYEE_COLUMNS, _format_employee_row)
