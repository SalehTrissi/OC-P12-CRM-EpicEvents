from EpicEventsCRM.models.employee_model import Employee, DepartmentEnum
from EpicEventsCRM.utils.permissions import has_permission
from EpicEventsCRM.utils.validators import (
    validate_email,
    validate_phone_number,
    validate_string_length,
)
from EpicEventsCRM.models.client_model import Client
from EpicEventsCRM.models.contract_model import Contract
from EpicEventsCRM.models.event_model import Event
from sqlalchemy.exc import IntegrityError
from auth import get_current_user
from db.database import get_db
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from getpass import getpass
from typing import Optional
from rich import box
import sentry_sdk


console = Console()


# --- Helper functions to keep code DRY ---
def _prompt_for_employee_data(employee: Optional[Employee] = None) -> dict:
    """
    Handles the interactive prompts to collect employee data.
    Uses existing employee data as defaults if provided (for updates).
    Returns a dictionary of the collected data.
    """
    data = {}

    # Use existing data as default if available, otherwise prompt for new
    data["first_name"] = Prompt.ask(
        "[bold yellow]First name[/bold yellow]", default=getattr(employee, 'first_name', None)
    )
    validate_string_length(data["first_name"], "First name", 50)

    data["last_name"] = Prompt.ask(
        "[bold yellow]Last name[/bold yellow]", default=getattr(employee, 'last_name', None)
    )
    validate_string_length(data["last_name"], "Last name", 50)

    while True:
        email = Prompt.ask("[bold yellow]Email[/bold yellow]",
                           default=getattr(employee, 'email', None))
        try:
            data["email"] = validate_email(email)
            break
        except ValueError as e:
            console.print(Panel(f"[bold red]{e}[/bold red]", box=box.ROUNDED))

    while True:
        phone = Prompt.ask("[bold yellow]Phone number[/bold yellow]",
                           default=getattr(employee, 'phone_number', None))
        try:
            data["phone_number"] = validate_phone_number(phone)
            break
        except ValueError as e:
            console.print(Panel(f"[bold red]{e}[/bold red]", box=box.ROUNDED))

    default_department_name = getattr(
        employee, 'department', DepartmentEnum.COMMERCIAL).name
    department_name = Prompt.ask(
        "[bold yellow]Department[/bold yellow]",
        choices=[d.name for d in DepartmentEnum],
        default=default_department_name,
    ).upper()
    data["department"] = DepartmentEnum[department_name]

    return data


def _commit_to_db(db, instance, success_message):
    """Handles the database commit and error logging."""
    try:
        db.add(instance)
        db.commit()
        db.refresh(instance)
        console.print(
            Panel(f"[bold green]{success_message}[/bold green]", box=box.ROUNDED))
        sentry_sdk.capture_message(success_message, level="info")
        return True
    except IntegrityError as e:
        db.rollback()
        console.print(Panel(
            "[bold red]Error: An employee with this email already exists.[/bold red]", box=box.ROUNDED))
        sentry_sdk.capture_exception(e)
        return False
    except Exception as e:
        db.rollback()
        console.print(
            Panel(f"[bold red]An unexpected error occurred: {e}[/bold red]", box=box.ROUNDED))
        sentry_sdk.capture_exception(e)
        return False


def _check_employee_dependencies(db, employee_id: int) -> Optional[str]:
    """
    Checks if an employee is assigned to any active records.
    Returns an error message string if dependencies are found, otherwise None.
    """
    dependencies = {
        "Clients": db.query(Client).filter_by(sales_contact_id=employee_id).first(),
        "Contracts": db.query(Contract).filter_by(sales_contact_id=employee_id).first(),
        "Events": db.query(Event).filter_by(support_contact_id=employee_id).first(),
    }

    active_dependencies = [name for name, found in dependencies.items() if found]

    if active_dependencies:
        error_msg = (
            "[bold red]Cannot delete this employee.[/bold red]\n"
            "They are still assigned to active records. Please reassign the following first:\n"
        )
        error_msg += "\n".join(f"- {name}" for name in active_dependencies)
        return error_msg
    return None


def _confirm_and_execute_deletion(db, employee_to_delete: Employee, current_user: Employee):
    """
    Asks for user confirmation and performs the deletion if confirmed.
    """
    emp_name = f"{employee_to_delete.first_name} {employee_to_delete.last_name}"
    confirmation = Prompt.ask(
        (
            f"[bold yellow]Are you sure you want to delete {emp_name} "
            f"(ID: {employee_to_delete.employee_id})? This action is irreversible.[/bold yellow]"
        ),
        choices=["yes", "no"],
        default="no"
    )

    if confirmation.lower() == "yes":
        db.delete(employee_to_delete)
        db.commit()
        console.print(Panel(
            f"[bold green]Employee {emp_name} has been successfully deleted.[/bold green]", box=box.ROUNDED))
        sentry_sdk.capture_message(
            (
                f"Employee '{emp_name}' (ID: {employee_to_delete.employee_id}) "
                f"deleted by {current_user.email}"
            ),
            level="info"
        )
    else:
        console.print(
            Panel("[bold cyan]Deletion cancelled.[/bold cyan]", box=box.ROUNDED))


# --- Public API Functions (Simple and Clean) ---
def create_employee():
    """Creates a new employee after checking permissions."""
    current_user = get_current_user()
    if not has_permission(current_user, "create_employee"):
        console.print(
            Panel("[bold red]Insufficient permissions.[/bold red]", box=box.ROUNDED))
        return

    console.print(Panel("[bold cyan]Create New Employee[/bold cyan]",
                  box=box.ROUNDED, style="bold green"))

    employee_data = _prompt_for_employee_data()

    console.print("[bold yellow]Enter password:[/bold yellow]")
    password = getpass(" ")
    if not password:
        console.print(
            Panel("[bold red]Password cannot be empty.[/bold red]", box=box.ROUNDED))
        return

    new_employee = Employee(**employee_data)
    new_employee.set_password(password)

    db = next(get_db())
    try:
        _commit_to_db(
            db, new_employee, f"Employee '{new_employee.first_name} {new_employee.last_name}' created successfully!")
    finally:
        db.close()


def update_employee(employee_id: int):
    """Updates an employee's details after checking permissions."""
    current_user = get_current_user()
    if not has_permission(current_user, "update_employee"):
        console.print(
            Panel("[bold red]Insufficient permissions.[/bold red]", box=box.ROUNDED))
        return

    db = next(get_db())
    try:
        employee_to_update = db.query(Employee).filter_by(
            employee_id=employee_id).first()
        if not employee_to_update:
            console.print(
                Panel("[bold red]Employee not found.[/bold red]", box=box.ROUNDED))
            return

        console.print(
            Panel(
                f"[bold cyan]Update Employee: {employee_to_update.first_name} "
                f"{employee_to_update.last_name}[/bold cyan]",
                box=box.ROUNDED,
                style="bold green"
            )
        )
        console.print(
            "[bold yellow](Leave blank to keep the current value.)[/bold yellow]\n")

        updated_data = _prompt_for_employee_data(employee=employee_to_update)

        # Update attributes from the collected data
        for key, value in updated_data.items():
            setattr(employee_to_update, key, value)

        change_password = Prompt.ask(
            "[bold yellow]Change password? (yes/no)[/bold yellow]",
            choices=["yes", "no"],
            default="no"
        )
        if change_password == "yes":
            password = getpass("Enter new password: ")
            if password:
                employee_to_update.set_password(password)

        _commit_to_db(db, employee_to_update,
                      f"Employee '{employee_to_update.first_name}' updated successfully!")

    finally:
        db.close()


def delete_employee(employee_id: int):
    """
    Deletes an employee after performing several safety checks.
    """
    current_user = get_current_user()
    if not current_user or not has_permission(current_user, "delete_employee"):
        console.print(Panel(
            "[bold red]You do not have permission to delete employees.[/bold red]", box=box.ROUNDED))
        return

    if getattr(current_user, "employee_id", None) == employee_id:
        console.print(
            Panel("[bold red]Error: You cannot delete your own account.[/bold red]", box=box.ROUNDED))
        return

    db = next(get_db())
    try:
        employee_to_delete = db.query(Employee).filter_by(
            employee_id=employee_id).first()
        if not employee_to_delete:
            console.print(
                Panel(f"[bold red]Employee with ID {employee_id} not found.[/bold red]", box=box.ROUNDED))
            return

        # Check for dependencies using the helper function
        dependency_error = _check_employee_dependencies(db, employee_id)
        if dependency_error:
            console.print(Panel(dependency_error, box=box.ROUNDED,
                          title="[bold red]Deletion Blocked[/bold red]"))
            return

        # Confirm and execute the deletion using the helper function
        _confirm_and_execute_deletion(db, employee_to_delete, current_user)

    except Exception as e:
        db.rollback()
        console.print(
            Panel(f"[bold red]An unexpected error occurred: {e}[/bold red]", box=box.ROUNDED))
        sentry_sdk.capture_exception(e)
    finally:
        db.close()
