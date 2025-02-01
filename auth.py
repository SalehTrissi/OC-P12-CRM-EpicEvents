from config import JWT_SECRET, JWT_ALGORITHM, JWT_EXP_DELTA_SECONDS
from EpicEventsCRM.utils.permissions import has_permission
from EpicEventsCRM.utils.validators import validate_email
from EpicEventsCRM.models.employee_model import Employee
from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import joinedload
from rich.progress import Progress
from rich.console import Console
from rich.prompt import Prompt
from db.database import get_db
from rich.panel import Panel
from getpass import getpass
from rich import box
import sentry_sdk
import time
import jwt
import os


console = Console()

# File to store the JWT token locally
TOKEN_FILE = ".epicevents_token"


def authenticate(email: str, password: str):
    """Authenticates a user and returns a JWT token if successful."""
    db = next(get_db())
    try:
        employee = db.query(Employee).filter_by(email=email.lower()).first()
        if employee and employee.verify_password(password):
            payload = {
                "employee_id": employee.employee_id,
                "exp": datetime.now(timezone.utc)
                + timedelta(seconds=JWT_EXP_DELTA_SECONDS),
            }
            token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
            return token
        return None
    except Exception as e:
        sentry_sdk.capture_exception(e)
        return None
    finally:
        db.close()


def decode_token(token: str):
    """Decode JWT token and handle exceptions for expired or invalid tokens."""
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except jwt.ExpiredSignatureError:
        console.print("[bold red]❌ Session expired. Please log in again.[/bold red]")
        delete_token()
        return None
    except jwt.InvalidTokenError:
        console.print("[bold red]❌ Invalid token. Please log in again.[/bold red]")
        delete_token()
        return None


def save_token(token: str):
    """Save the JWT token to a local file."""
    with open(TOKEN_FILE, "w") as f:
        f.write(token)


def load_token():
    """Load JWT token from a local file."""
    try:
        with open(TOKEN_FILE, "r") as f:
            return f.read()
    except FileNotFoundError:
        return None


def delete_token():
    """Remove the JWT token from the local file."""
    if os.path.exists(TOKEN_FILE):
        os.remove(TOKEN_FILE)


def get_current_user():
    """Retrieve the currently authenticated user from the stored token."""
    token = load_token()
    if token:
        payload = decode_token(token)
        if payload:
            employee_id = payload.get("employee_id")
            db = next(get_db())
            try:
                return (
                    db.query(Employee)
                    .options(
                        joinedload(Employee.clients),
                        joinedload(Employee.contracts),
                        joinedload(Employee.events),
                    )
                    .filter_by(employee_id=employee_id)
                    .first()
                )
            except Exception as e:
                sentry_sdk.capture_exception(e)
                return None
            finally:
                db.close()
    return None


def is_authorized(permission_name: str):
    """Check if the current user has the specified permission."""
    employee = get_current_user()
    return employee and has_permission(employee, permission_name)


def login():
    """Handles user login with an interactive interface."""
    while True:
        console.print(
            Panel(
                "[bold cyan]Welcome to Epic Events CRM Login[/bold cyan]",
                box=box.ROUNDED,
                style="bold green",
            ),
            justify="center",
        )

        while True:
            email = (
                Prompt.ask("[bold yellow]Enter your Email[/bold yellow]")
                .strip()
                .lower()
            )
            if not email:
                console.print(
                    "[bold red]❌ Email cannot be empty! Please enter a valid email."
                    "[/bold red]"
                )
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

        token = authenticate(email, password)
        if token:
            save_token(token)
            user = get_current_user()

            if user:
                console.print(
                    Panel(
                        f"✅ [bold green]Authentication successful![/bold green]\n"
                        f"Welcome back, [bold yellow]{user.first_name} {
                            user.last_name}[/bold yellow]!",
                        box=box.DOUBLE,
                        style="green",
                    ),
                    justify="center",
                )
            else:
                console.print(
                    Panel(
                        "✅ [bold green]Authentication successful![/bold green]",
                        box=box.DOUBLE,
                        style="green",
                    ),
                    justify="center",
                )

            return
        else:
            console.print(
                Panel(
                    "❌ [bold red]Authentication failed! Please check your credentials."
                    "[/bold red]",
                    box=box.DOUBLE,
                    style="red",
                ))

            retry_prompt = Prompt.ask(
                "[bold yellow]Would you like to try again? (yes/no)[/bold yellow]",
                default="yes",
            )
            if retry_prompt.strip().lower() == "no":
                console.print("[bold red]Exiting... Have a great day![/bold red]")
                return


def logout():
    """Handles user logout with a professional interface."""
    if os.path.exists(TOKEN_FILE):
        delete_token()
        console.print(
            Panel(
                "👋 [bold cyan]You have successfully logged out![/bold cyan]\n"
                "[bold green]Thank you for using Epic Events CRM.[/bold green]",
                box=box.ROUNDED,
                style="bold green",
            )
        )
    else:
        console.print(
            Panel(
                "⚠️ [bold yellow]You are already logged out![/bold yellow]\n"
                "[dim]No active session was found.[/dim]",
                box=box.ROUNDED,
                style="yellow",
            )
        )


def status():
    """Displays the login status of the current user."""
    user = get_current_user()
    if user:
        console.print(
            Panel(
                f"✅ [bold green]Logged in as[/bold green]\n"
                f"[bold yellow]{user.first_name} {user.last_name}[/bold yellow]\n"
                f"[bold cyan]Department:[/bold cyan] {user.department.value}\n"
                f"[bold cyan]Email:[/bold cyan] {user.email}\n"
                f"[bold cyan]Phone Number:[/bold cyan] {user.phone_number}\n\n"
                f"[bold magenta]Related Data:[/bold magenta]\n"
                f"- Clients: {len(user.clients)}\n"
                f"- Contracts: {len(user.contracts)}\n"
                f"- Events: {len(user.events)}",
                box=box.ROUNDED,
                style="bold green",
            )
        )
    else:
        console.print(
            Panel(
                "❌ [bold red]You are not logged in.[/bold red]\n"
                "Please log in to access your account.",
                box=box.ROUNDED,
                style="red",
            )
        )
