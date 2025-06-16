from EpicEventsCRM.utils.validators import (
    validate_email,
    validate_phone_number,
    validate_string_length,
)
from EpicEventsCRM.models.employee_model import Employee, DepartmentEnum
from EpicEventsCRM.utils.permissions import has_permission
from sqlalchemy.exc import IntegrityError
from auth import get_current_user
from rich.console import Console
from rich.prompt import Prompt
from db.database import get_db
from rich.panel import Panel
from getpass import getpass
from rich import box
import sentry_sdk


console = Console()


def create_employee():
    """Creates a new employee interactively with validation and database integration."""
    current_user = get_current_user()

    if not current_user:
        console.print(
            Panel("[bold red]Authentication required.[/bold red]", box=box.ROUNDED)
        )
        return

    if not has_permission(current_user, "manage_users"):
        console.print(
            Panel("[bold red]Insufficient permissions.[/bold red]", box=box.ROUNDED)
        )
        return

    console.print(
        Panel(
            "[bold cyan]Create New Employee[/bold cyan]",
            box=box.ROUNDED,
            style="bold green",
        )
    )

    # Collect employee information
    first_name = Prompt.ask("[bold yellow]Enter first name[/bold yellow]")
    validate_string_length(first_name, "First name", 50)

    last_name = Prompt.ask("[bold yellow]Enter last name[/bold yellow]")
    validate_string_length(last_name, "Last name", 50)

    # Validate email
    while True:
        email = Prompt.ask("[bold yellow]Enter email address[/bold yellow]")
        try:
            validate_email(email)
            break
        except ValueError as e:
            console.print(Panel(f"[bold red]{e}[/bold red]", box=box.ROUNDED))

    # Validate phone number
    while True:
        phone_number = Prompt.ask("[bold yellow]Enter phone number[/bold yellow]")
        try:
            validate_phone_number(phone_number)
            break
        except ValueError as e:
            console.print(Panel(f"[bold red]{e}[/bold red]", box=box.ROUNDED))

    # Validate department
    department_input = Prompt.ask(
        "[bold yellow]Select department (COMMERCIAL, SUPPORT, MANAGEMENT)"
        "[/bold yellow]",
        choices=[
            "COMMERCIAL",
            "SUPPORT",
            "MANAGEMENT"],
        default="COMMERCIAL",
    ).upper()
    department = DepartmentEnum[department_input]

    # Secure password input
    console.print("[bold yellow]Enter password:[/bold yellow]")
    password = getpass(" ")
    if not password:
        console.print(
            Panel("[bold red]Password cannot be empty.[/bold red]", box=box.ROUNDED)
        )
        return

    # Create employee object
    employee = Employee(
        first_name=first_name,
        last_name=last_name,
        email=email,
        phone_number=phone_number,
        department=department,
    )
    employee.set_password(password)

    # Save to database
    db = next(get_db())
    try:
        db.add(employee)
        db.commit()
        console.print(
            Panel(
                f"[bold green]Employee '{first_name} {
                    last_name}' created successfully![/bold green]",
                box=box.ROUNDED,
            )
        )
        sentry_sdk.capture_message(
            f"Employee '{first_name} {
                last_name}' created successfully!",
            level="info",
        )
    except IntegrityError as e:
        db.rollback()
        console.print(
            Panel(
                "[bold red]Error: An employee with this email already exists."
                "[/bold red]",
                box=box.ROUNDED,
            ))
        sentry_sdk.capture_exception(e)
    except Exception as e:
        db.rollback()
        console.print(
            Panel(
                f"[bold red]Unexpected error: {
                    e}[/bold red]",
                box=box.ROUNDED,
            )
        )
        sentry_sdk.capture_exception(e)
    finally:
        db.close()


def update_employee(employee_id):
    """Updates an employee interactively with validation and error handling."""
    current_user = get_current_user()

    if not current_user:
        console.print(
            Panel("[bold red]Authentication required.[/bold red]", box=box.ROUNDED)
        )
        return

    if not has_permission(current_user, "manage_users"):
        console.print(
            Panel("[bold red]Insufficient permissions.[/bold red]", box=box.ROUNDED)
        )
        return

    db = next(get_db())

    try:
        employee = db.query(Employee).filter_by(employee_id=employee_id).first()
        if not employee:
            console.print(
                Panel("[bold red]Employee not found.[/bold red]", box=box.ROUNDED)
            )
            sentry_sdk.capture_message(
                f"Employee with ID '{employee_id}' not found.", level="warning"
            )
            return

        console.print(
            Panel(
                f"[bold cyan]Update Employee: {employee.first_name} {
                    employee.last_name}[/bold cyan]",
                box=box.ROUNDED,
                style="bold green",
            )
        )
        console.print(
            "[bold yellow](Leave blank to keep the current value.)[/bold yellow]\n"
        )

        # Collecting new information
        first_name = Prompt.ask(
            "[bold yellow]First name[/bold yellow]", default=employee.first_name
        )
        last_name = Prompt.ask(
            "[bold yellow]Last name[/bold yellow]", default=employee.last_name
        )

        while True:
            email = Prompt.ask(
                "[bold yellow]Email[/bold yellow]", default=employee.email
            )
            try:
                validate_email(email)
                break
            except ValueError as e:
                console.print(Panel(f"[bold red]{e}[/bold red]", box=box.ROUNDED))

        phone_number = Prompt.ask(
            "[bold yellow]Phone number[/bold yellow]", default=employee.phone_number
        )

        department_input = Prompt.ask(
            "[bold yellow]Department[/bold yellow]",
            choices=["COMMERCIAL", "SUPPORT", "MANAGEMENT"],
            default=employee.department.name,
        ).upper()
        department = DepartmentEnum[department_input]

        # Prompt for password change
        change_password = Prompt.ask(
            "[bold yellow]Do you want to change the password? (yes/no)[/bold yellow]",
            choices=["yes", "no"],
            default="no",
        ).lower()
        if change_password == "yes":
            console.print("[bold yellow]Enter new password:[/bold yellow]")
            password = getpass(" ")
            if password:
                employee.set_password(password)
            else:
                console.print(
                    Panel(
                        "[bold red]Password cannot be empty.[/bold red]",
                        box=box.ROUNDED,
                    )
                )

        # Update employee details
        setattr(employee, "first_name", first_name)
        setattr(employee, "last_name", last_name)
        setattr(employee, "email", email)
        setattr(employee, "phone_number", phone_number)
        setattr(employee, "department", department)

        # Save changes to database
        db.commit()
        console.print(
            Panel(
                f"[bold green]Employee '{first_name} {
                    last_name}' updated successfully![/bold green]",
                box=box.ROUNDED,
            )
        )
        sentry_sdk.capture_message(
            f"Employee '{first_name} {
                last_name}' updated successfully!",
            level="info",
        )

    except IntegrityError as e:
        db.rollback()
        console.print(
            Panel(
                "[bold red]Error: An employee with this email already exists."
                "[/bold red]",
                box=box.ROUNDED,
            ))
        sentry_sdk.capture_exception(e)
    except Exception as e:
        db.rollback()
        console.print(
            Panel(
                f"[bold red]Unexpected error: {
                    e}[/bold red]",
                box=box.ROUNDED,
            )
        )
        sentry_sdk.capture_exception(e)
    finally:
        db.close()
