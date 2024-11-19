from EpicEventsCRM.models.employee_model import Employee, DepartmentEnum
from sqlalchemy.exc import IntegrityError
from db.database import SessionLocal
from getpass import getpass
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from rich import box

console = Console()


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
    first_name = Prompt.ask("[bold yellow]First name[/bold yellow]")
    last_name = Prompt.ask("[bold yellow]Last name[/bold yellow]")
    email = Prompt.ask("[bold yellow]Email[/bold yellow]")
    phone_number = Prompt.ask("[bold yellow]Phone number[/bold yellow]")
    department_input = Prompt.ask(
        "[bold yellow]Department (COMMERCIAL/SUPPORT/MANAGEMENT)[/bold yellow]",
        choices=["COMMERCIAL", "SUPPORT", "MANAGEMENT"],
        default="COMMERCIAL"
    ).upper()

    console.print("[bold yellow]Enter password below:[/bold yellow]")
    password = getpass("Password: ")

    # Verify department
    if department_input not in DepartmentEnum.__members__:
        console.print(
            Panel("[bold red]Invalid department. Please choose from COMMERCIAL, SUPPORT, or MANAGEMENT.[/bold red]",
                  box=box.ROUNDED)
        )
        return

    department = DepartmentEnum[department_input]

    # Create the Employee object
    employee = Employee(
        first_name=first_name,
        last_name=last_name,
        email=email,
        phone_number=phone_number,
        department=department
    )
    employee.set_password(password)

    # Save to the database
    with SessionLocal() as session:
        session.add(employee)
        try:
            session.commit()
            console.print(
                Panel("[bold green]Employee created successfully![/bold green]",
                      box=box.ROUNDED)
            )
        except IntegrityError:
            session.rollback()
            console.print(
                Panel(
                    "[bold red]Error: An employee with this email already exists.[/bold red]", box=box.ROUNDED)
            )
        except Exception as e:
            session.rollback()
            console.print(
                Panel(f"[bold red]Error creating employee: {
                      e}[/bold red]", box=box.ROUNDED)
            )


# Run the script interactively
if __name__ == "__main__":
    create_employee_interactive()
