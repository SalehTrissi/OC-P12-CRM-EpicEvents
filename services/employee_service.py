from EpicEventsCRM.models.employee_model import Employee, DepartmentEnum
from EpicEventsCRM.utils.permissions import has_permission
from sqlalchemy.exc import IntegrityError
from db.database import SessionLocal
from auth import get_current_user
from getpass import getpass
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from rich import box

console = Console()


def create_employee():
    """
    Creates a new employee with a user-friendly and visually appealing interface.
    """
    current_user = get_current_user()
    if not current_user:
        console.print(
            Panel("[bold red]You must be authenticated to create an employee.[/bold red]", box=box.ROUNDED))
        return

    if not has_permission(current_user, 'manage_users'):
        console.print(
            Panel("[bold red]You do not have permission to create an employee.[/bold red]", box=box.ROUNDED))
        return

    console.print(Panel("[bold cyan]Create New Employee[/bold cyan]",
                        box=box.ROUNDED, style="bold green"))

    # Collect employee information
    first_name = Prompt.ask("[bold yellow]Enter first name[/bold yellow]")
    last_name = Prompt.ask("[bold yellow]Enter last name[/bold yellow]")
    email = Prompt.ask("[bold yellow]Enter email address[/bold yellow]")
    phone_number = Prompt.ask("[bold yellow]Enter phone number[/bold yellow]")
    department_input = Prompt.ask(
        "[bold yellow]Select department (COMMERCIAL, SUPPORT, MANAGEMENT)[/bold yellow]",
        choices=["COMMERCIAL", "SUPPORT", "MANAGEMENT"],
        default="COMMERCIAL"
    ).upper()
    console.print("[bold yellow]Enter password:[/bold yellow]", end="")
    password = getpass(" ")

    # Verify department
    department = DepartmentEnum[department_input]

    # Create employee object
    employee = Employee(
        first_name=first_name,
        last_name=last_name,
        email=email,
        phone_number=phone_number,
        department=department
    )
    employee.set_password(password)

    # Save to database
    with SessionLocal as session:
        session.add(employee)
        try:
            session.commit()
            console.print(
                Panel(f"[bold green]Employee '{first_name} {last_name}' created successfully![/bold green]",
                      box=box.ROUNDED))
        except IntegrityError:
            session.rollback()
            console.print(Panel(
                "[bold red]Error: An employee with this email already exists.[/bold red]", box=box.ROUNDED))
        except Exception as e:
            session.rollback()
            console.print(Panel(f"[bold red]Error creating employee: {
                          e}[/bold red]", box=box.ROUNDED))


def update_employee(employee_id):
    """
    Updates an employee's information with a user-friendly and visually appealing interface.
    """
    current_user = get_current_user()
    if not current_user:
        console.print(
            Panel("[bold red]You must be authenticated to update an employee.[/bold red]", box=box.ROUNDED))
        return

    if not has_permission(current_user, 'manage_users'):
        console.print(
            Panel("[bold red]You do not have permission to update an employee.[/bold red]", box=box.ROUNDED))
        return

    with SessionLocal as session:
        employee = session.query(Employee).filter_by(employee_id=employee_id).first()
        if not employee:
            console.print(
                Panel("[bold red]Employee not found.[/bold red]", box=box.ROUNDED))
            return

        console.print(Panel(f"[bold cyan]Update Employee: {employee.first_name} {employee.last_name}[/bold cyan]",
                            box=box.ROUNDED, style="bold green"))

        console.print(
            "[bold yellow](Leave blank to keep the current value.)[/bold yellow]\n")

        # Collecting new information
        first_name = Prompt.ask(
            f"[bold yellow]First name[/bold yellow] [bold green](current: {
                employee.first_name})[/bold green]",
            default=employee.first_name,
            show_default=False
        )
        last_name = Prompt.ask(
            f"[bold yellow]Last name[/bold yellow] [bold green](current: {
                employee.last_name})[/bold green]",
            default=employee.last_name,
            show_default=False
        )
        email = Prompt.ask(
            f"[bold yellow]Email[/bold yellow] [bold green](current: {
                employee.email})[/bold green]",
            default=employee.email,
            show_default=False
        )
        phone_number = Prompt.ask(
            f"[bold yellow]Phone number[/bold yellow] [bold green](current: {
                employee.phone_number})[/bold green]",
            default=employee.phone_number,
            show_default=False
        )
        department_input = Prompt.ask(
            f"[bold yellow]Department[/bold yellow] [bold green](current: {
                employee.department.name})[/bold green]",
            choices=["COMMERCIAL", "SUPPORT", "MANAGEMENT"],
            default=employee.department.name,
            show_default=False
        ).upper()

        # Verify department
        department = DepartmentEnum[department_input]

        # Update employee details
        employee.first_name = first_name
        employee.last_name = last_name
        employee.email = email
        employee.phone_number = phone_number
        employee.department = department

        # Prompt for password change
        change_password = Prompt.ask(
            "[bold yellow]Do you want to change the password?[/bold yellow]",
            choices=["yes", "no"],
            default="no",
            show_default=False
        ).lower()
        if change_password == "yes":
            console.print("[bold yellow]Enter new password:[/bold yellow]", end="")
            password = getpass(" ")
            employee.set_password(password)

        # Save changes to database
        try:
            session.commit()
            console.print(
                Panel(f"[bold green]Employee '{first_name} {last_name}' updated successfully![/bold green]",
                      box=box.ROUNDED))
        except IntegrityError:
            session.rollback()
            console.print(Panel(
                "[bold red]Error: An employee with this email already exists.[/bold red]", box=box.ROUNDED))
        except Exception as e:
            session.rollback()
            console.print(Panel(f"[bold red]Error updating employee: {
                          e}[/bold red]", box=box.ROUNDED))
