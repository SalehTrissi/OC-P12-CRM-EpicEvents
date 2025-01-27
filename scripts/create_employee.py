from EpicEventsCRM.models.employee_model import Employee, DepartmentEnum
from sqlalchemy.exc import IntegrityError
from db.database import SessionLocal
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
import config  # noqa: F401
from getpass import getpass
from rich import box
import sentry_sdk


console = Console()


def prompt_required_input(prompt_message, allow_empty=False):
    """
    Prompt the user for input and validate that it is not empty.
    """
    while True:
        user_input = Prompt.ask(f"[bold yellow]{prompt_message}[/bold yellow]").strip()
        if allow_empty or user_input:
            return user_input
        else:
            console.print(
                Panel("[bold red]Error: This field cannot be empty.[/bold red]",
                      box=box.ROUNDED)
            )


def create_employee_interactive():
    """
    Interactive script to create a new employee with a user-friendly interface.
    """
    console.print(
        Panel(
            "[bold cyan]Create a New Employee[/bold cyan]",
            box=box.ROUNDED,
            style="bold green"
        )
    )

    # Collect employee information interactively
    first_name = prompt_required_input("First name")
    last_name = prompt_required_input("Last name")
    email = prompt_required_input("Email")
    phone_number = prompt_required_input("Phone number")

    # Prompt for department with case-insensitivity
    while True:
        department_input = Prompt.ask(
            "[bold yellow]Department (COMMERCIAL/SUPPORT/MANAGEMENT)[/bold yellow]",
            default="COMMERCIAL"
        ).strip().upper()

        # Validate the department input
        if department_input in DepartmentEnum.__members__:
            break
        console.print(
            Panel("[bold red]Invalid department. Please choose from "
                  "COMMERCIAL, SUPPORT, or MANAGEMENT.[/bold red]", box=box.ROUNDED)
        )

    # Prompt for password securely
    console.print("[bold yellow]Enter password below:[/bold yellow]")
    password = getpass("Password: ").strip()
    if not password:
        console.print(
            "[bold red]Password cannot be empty."
            " Please provide a valid password.[/bold red]")
        return

    # Create the Employee object
    try:
        employee = Employee(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone_number=phone_number,
            department=DepartmentEnum[department_input]
        )
        employee.set_password(password)

        # Save the employee to the database
        session = SessionLocal
        try:
            session.add(employee)
            session.commit()
            console.print(
                Panel("[bold green]Employee created successfully![/bold green]",
                      box=box.ROUNDED)
            )
        except IntegrityError as e:
            session.rollback()
            console.print(
                Panel("[bold red]Error: An employee with this email already exists."
                      "[/bold red]", box=box.ROUNDED)
            )
            sentry_sdk.capture_exception(e)
        except Exception as e:
            session.rollback()
            console.print(
                Panel(f"[bold red]An unexpected error occurred: {
                      e}[/bold red]", box=box.ROUNDED)
            )
            sentry_sdk.capture_exception(e)
        finally:
            session.close()
    except ValueError as e:
        console.print(
            Panel(f"[bold red]Error: {e}[/bold red]", box=box.ROUNDED)
        )
        sentry_sdk.capture_exception(e)


# Run the script interactively
if __name__ == "__main__":
    create_employee_interactive()
