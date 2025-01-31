from sqlalchemy.orm import joinedload
from config import JWT_SECRET, JWT_ALGORITHM, JWT_EXP_DELTA_SECONDS
from EpicEventsCRM.utils.permissions import has_permission
from EpicEventsCRM.utils.validators import validate_email
from EpicEventsCRM.models.employee_model import Employee
from datetime import datetime, timedelta, timezone
from db.database import SessionLocal

from sqlalchemy.orm import Session
from rich.progress import Progress

from rich.console import Console

from rich.prompt import Prompt
from rich.panel import Panel
from getpass import getpass
from rich import box
import time
import jwt
import os


console = Console()

# File to store the JWT token locally
TOKEN_FILE = '.epicevents_token'


def authenticate(session: Session, email: str, password: str):
    """
    Authenticates a user by verifying their credentials.
    Returns a JWT token if authentication is successful.
    """
    employee = session.query(Employee).filter_by(email=email.lower()).first()
    if employee and employee.verify_password(password):
        payload = {
            'employee_id': employee.employee_id,
            'exp': datetime.now(timezone.utc) + timedelta(seconds=JWT_EXP_DELTA_SECONDS)
        }
        token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
        return token
    else:
        return None


def decode_token(token: str):
    """
    Decode JWT token to retrieve user information.
    Handle exceptions in case of expired or invalid token.
    """
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        # The token has expired
        print("Your session has expired. Please log in again.")
        delete_token()
        return None
    except jwt.ExpiredSignatureError:
        # The token is invalid
        print("Invalid token. Please log in again.")
        delete_token()
        return None


def save_token(token: str):
    """
    Save the token to a local file.
    """
    with open(TOKEN_FILE, 'w') as f:
        f.write(token)


def load_token():
    """
    Loads token from local file.
    """
    try:
        with open(TOKEN_FILE, 'r') as f:
            token = f.read()
            return token
    except FileNotFoundError:
        return None


def delete_token():
    """
    Removes the token from the local file.
    """
    if os.path.exists(TOKEN_FILE):
        os.remove(TOKEN_FILE)


def get_current_user():
    """
    Gets the currently authenticated user from the stored token.
    """
    token = load_token()
    if token:
        payload = decode_token(token)
        if payload:
            employee_id = payload.get('employee_id')
            # Create a session to access the database
            with SessionLocal as session:
                employee = session.query(Employee).options(
                    joinedload(Employee.clients),
                    joinedload(Employee.contracts),
                    joinedload(Employee.events)
                ).filter_by(employee_id=employee_id).first()
                return employee
    return None


def is_authorized(permission_name: str):
    """
    Checks if the current user has the specified permission.
    """
    employee = get_current_user()
    if employee and has_permission(employee, permission_name):
        return True
    else:
        return False


def login():
    """
    Handles the user login process with a stylish and professional interface.
    """
    while True:
        console.print(Panel("[bold cyan]Welcome to Epic Events CRM Login[/bold cyan]",
                            box=box.ROUNDED, style="bold green", expand=False), justify="center")

        while True:
            email = Prompt.ask(
                "[bold yellow]Enter your Email[/bold yellow]").strip().lower()
            if not email:
                console.print(
                    "[bold red]❌ Email cannot be empty! Please enter a valid email.[/bold red]")
                continue

            try:
                email = validate_email(email)
                break
            except ValueError as e:
                console.print(f"[bold red]❌ {str(e)}[/bold red]")

        console.print("[bold yellow]Enter your Password:[/bold yellow]", end=" ")
        password = getpass("")

        with Progress() as progress:
            task = progress.add_task("[cyan]Authenticating...", total=100)
            for _ in range(10):
                time.sleep(0.1)
                progress.update(task, advance=10)

        # Create a session to access the database
        with SessionLocal as session:
            token = authenticate(session, email, password)

        if token:
            save_token(token)
            console.print(
                Panel(":white_check_mark:"
                      " [bold green]Authentication successful![/bold green]\n"
                      "Welcome back, [bold yellow]{}[/bold yellow]!".format(email),
                      box=box.DOUBLE, style="green", expand=False))
            return
        else:
            console.print(
                Panel(":x: [bold red]Authentication failed!"
                      " Please check your credentials.[/bold red]",
                      box=box.DOUBLE, style="red", expand=False))

            # Suggest retrying
            retry_prompt = Prompt.ask(
                "[bold yellow]Would you like to try again? (yes/no)[/bold yellow]", default="yes")
            if retry_prompt.strip().lower() == "yes":
                console.print("\n[bold green]Let's try again![/bold green]")
                continue
            else:
                console.print("\n[bold red]Exiting... Have a great day![/bold red]")
                return


def logout():
    """
    Manages the user logout process with a professional and styled interface.
    """
    if os.path.exists(TOKEN_FILE):
        # Simulate logout process
        delete_token()
        console.print(
            Panel(
                ":wave: [bold cyan]You have successfully logged out![/bold cyan]\n"
                "[bold green]Thank you for using Epic Events CRM.[/bold green]\n"
                "[dim]See you next time![/dim]",
                box=box.ROUNDED, style="bold green", expand=False
            )
        )
        return
    else:
        console.print(
            Panel(
                ":warning: [bold yellow]You are already logged out![/bold yellow]\n"
                "[dim]No active session was found.[/dim]",
                box=box.ROUNDED, style="yellow", expand=False
            )
        )
        return


def status():
    """
    Displays the login status of the current user with a professional interface.
    """
    user = get_current_user()
    if user:
        # Get related entity counts
        num_clients = len(user.clients)
        num_contracts = len(user.contracts)
        num_events = len(user.events)

        # Display user details
        console.print(
            Panel(
                f":white_check_mark: [bold green]Logged in as[/bold green]\n"
                f"[bold yellow]{user.first_name} {user.last_name}[/bold yellow]\n"
                f"[bold cyan]Department:[/bold cyan] {user.department.value}\n"
                f"[bold cyan]Email:[/bold cyan] {user.email}\n"
                f"[bold cyan]Phone Number:[/bold cyan] {user.phone_number}\n\n"
                f"[bold magenta]Related Data:[/bold magenta]\n"
                f"- Clients: {num_clients}\n"
                f"- Contracts: {num_contracts}\n"
                f"- Events: {num_events}",
                box=box.ROUNDED, style="bold green", expand=False
            )
        )
    else:
        console.print(
            Panel(":x: [bold red]You are not logged in.[/bold red]\n"
                  "Please log in to access your account.",
                  box=box.ROUNDED, style="red", expand=False)
        )
