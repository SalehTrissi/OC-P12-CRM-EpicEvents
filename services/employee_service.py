from EpicEventsCRM.models.employee_model import Employee, DepartmentEnum
from EpicEventsCRM.utils.permissions import has_permission
from EpicEventsCRM.utils.validators import (
    validate_email,
    validate_phone_number,
    validate_string_length,
)
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

    department_name = Prompt.ask(
        "[bold yellow]Department[/bold yellow]",
        choices=[d.name for d in DepartmentEnum],
        default=getattr(employee, 'department', DepartmentEnum.COMMERCIAL).name,
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
