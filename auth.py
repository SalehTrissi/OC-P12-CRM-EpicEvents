from config import JWT_SECRET, JWT_ALGORITHM, JWT_EXP_DELTA_SECONDS
from EpicEventsCRM.utils.permissions import has_permission
from EpicEventsCRM.models.employee_model import Employee
from datetime import datetime, timedelta, timezone
from db.database import SessionLocal
from sqlalchemy.orm import Session
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from getpass import getpass
from rich import box
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
                employee = session.query(Employee).filter_by(
                    employee_id=employee_id).first()
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
    console.print(Panel("[bold cyan]Welcome to Epic Events CRM Login[/bold cyan]",
                        box=box.ROUNDED, style="bold green", expand=False))

    email = Prompt.ask("[bold yellow]Enter your Email[/bold yellow]").strip().lower()

    # Display the password prompt using Rich and pass a plain string to getpass
    console.print("[bold yellow]Enter your Password:[/bold yellow]", end="")
    password = getpass(" ")

    # Simulate authentication process with a progress bar
    console.print("\n[bold yellow]Authenticating...[/bold yellow]\n", style="dim")

    # Create a session to access the database
    with SessionLocal as session:
        token = authenticate(session, email, password)

    if token:
        save_token(token)
        console.print(
            Panel(":white_check_mark: [bold green]Authentication successful![/bold green]\n"
                  "Welcome back, [bold yellow]{}[/bold yellow]!".format(email),
                  box=box.DOUBLE, style="green", expand=False))
    else:
        console.print(
            Panel(":x: [bold red]Authentication failed! Please check your credentials.[/bold red]",
                  box=box.DOUBLE, style="red", expand=False))

        # Suggest retrying
        retry_prompt = Prompt.ask(
            "[bold yellow]Would you like to try again? (yes/no)[/bold yellow]", default="yes")
        if retry_prompt.strip().lower() == "yes":
            console.print("\n[bold green]Let's try again![/bold green]")
            login()
        else:
            console.print("\n[bold red]Exiting... Have a great day![/bold red]")


def logout():
    """
    Manages the user logout process with a professional and styled interface.
    """
    if os.path.exists(TOKEN_FILE):
        # Simulate logout process
        delete_token()
        console.print(
            Panel(":wave: [bold cyan]You are successfully logged out.[/bold cyan]\n"
                  "See you next time!",
                  box=box.ROUNDED, style="bold green", expand=False)
        )
    else:
        console.print(
            Panel(":warning: [bold yellow]You are already logged out![/bold yellow]\n"
                  "No active session found.",
                  box=box.ROUNDED, style="yellow", expand=False)
        )


def status():
    """
    Displays the login status of the current user.
    """
    user = get_current_user()
    if user:
        print(f"Logged in as {user.first_name} {
              user.last_name} ({user.department.value})")
    else:
        print("You are not logged in.")
