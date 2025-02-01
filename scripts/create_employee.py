from EpicEventsCRM.models.employee_model import Employee, DepartmentEnum
from EpicEventsCRM.utils.validators import validate_email
from sqlalchemy.exc import IntegrityError
from rich.console import Console
from db.database import get_db
from rich.prompt import Prompt
from rich.panel import Panel
from getpass import getpass
from rich import box
import sentry_sdk


console = Console()


def prompt_required_input(prompt_message, allow_empty=False):
    """Prompt the user for input and validate that it is not empty."""
    while True:
        user_input = Prompt.ask(f"[bold yellow]{prompt_message}[/bold yellow]").strip()
        if allow_empty or user_input:
            return user_input
        else:
            console.print(
                Panel(
                    "[bold red]Error: This field cannot be empty.[/bold red]",
                    box=box.ROUNDED,
                )
            )


def create_employee_interactive():
    """Interactive script to create a new employee."""
    console.print(
        Panel(
            "[bold cyan]Create a New Employee[/bold cyan]",
            box=box.ROUNDED,
            style="bold green",
        )
    )

    # Collect employee information interactively
    first_name = prompt_required_input("First name")
    last_name = prompt_required_input("Last name")

    # Validate email
    while True:
        email = prompt_required_input("Email")
        try:
            validate_email(email)
            break
        except ValueError as e:
            console.print(Panel(f"[bold red]Error: {e}[/bold red]", box=box.ROUNDED))

    phone_number = prompt_required_input("Phone number")

    # Prompt for department
    while True:
        department_input = (
            Prompt.ask(
                "[bold yellow]Department (COMMERCIAL/SUPPORT/MANAGEMENT)[/bold yellow]",
                default="COMMERCIAL",
            )
            .strip()
            .upper()
        )

        # Validate the department input
        if department_input in DepartmentEnum.__members__:
            break
        console.print(
            Panel(
                "[bold red]Invalid department. Please choose from COMMERCIAL,"
                " SUPPORT, or MANAGEMENT."
                "[/bold red]",
                box=box.ROUNDED,
            ))

    # Secure password prompt
    console.print("[bold yellow]Enter password below:[/bold yellow]")
    password = getpass("Password: ").strip()
    if not password:
        console.print(
            "[bold red]Password cannot be empty."
            " Please provide a valid password.[/bold red]"
        )
        return

    # Create employee and save to DB
    employee = Employee(
        first_name=first_name,
        last_name=last_name,
        email=email,
        phone_number=phone_number,
        department=DepartmentEnum[department_input],
    )
    employee.set_password(password)

    # Using get_db() to ensure proper session management
    db = next(get_db())
    try:
        db.add(employee)
        db.commit()
        console.print(
            Panel(
                "[bold green]Employee created successfully![/bold green]",
                box=box.ROUNDED,
            )
        )
    except IntegrityError:
        db.rollback()
        console.print(
            Panel(
                "[bold red]Error: An employee with this email already exists."
                "[/bold red]",
                box=box.ROUNDED,
            ))
        sentry_sdk.capture_exception(IntegrityError)
    except Exception as e:
        db.rollback()
        console.print(
            Panel(
                f"[bold red]An unexpected error occurred: {
                    e}[/bold red]",
                box=box.ROUNDED,
            )
        )
        sentry_sdk.capture_exception(e)
    finally:
        db.close()


# Run the script interactively
if __name__ == "__main__":
    create_employee_interactive()
