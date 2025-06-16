from EpicEventsCRM.utils.permissions import get_available_commands
from auth import get_current_user
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box


console = Console()


def _display_welcome_panel(employee=None):
    """Displays a welcome panel appropriate to the login state."""
    if employee:
        panel_content = (
            f"[bold cyan]Welcome, {employee.first_name}[/bold cyan] "
            f"[bold green]({employee.department.value})[/bold green]"
        )
        panel = Panel(panel_content, box=box.HEAVY, style="bold green", expand=True)
    else:
        panel_content = (
            "[bold cyan]Welcome to Epic Events CRM[/bold cyan]\n"
            "[bold yellow]You are not logged in.[/bold yellow]\n"
            "[bold green]Please log in to access more commands.[/bold green]"
        )
        panel = Panel(panel_content, box=box.DOUBLE, style="bold green", expand=True)

    console.print(panel, justify="center")
    console.print("\n")


def _get_commands_for_user(employee=None):
    """Retrieves the appropriate command dictionary based on the user."""
    if employee:
        return dict(get_available_commands(employee))
    else:
        # Commands for non-logged-in users
        return {
            "menu": "Display the main menu again.",
            "login": "Log in to the system.",
            "help": "Display help for commands.",
        }


def _build_and_display_table(commands_dict: dict):
    """Builds and displays the formatted command table."""
    table = Table(
        title="[bold magenta]📜 Available Commands[/bold magenta]",
        box=box.ROUNDED,
        header_style="bold magenta",
        expand=True,
    )
    table.add_column("No.", justify="center", style="bold yellow", width=5)
    table.add_column("Command", justify="left", style="cyan", min_width=20)
    table.add_column("Description", justify="left", style="green")

    for idx, (command, description) in enumerate(commands_dict.items(), start=1):
        parts = command.split(" ", 1)
        base_command = parts[0]
        args = f" [dim italic]{parts[1]}[/dim italic]" if len(parts) > 1 else ""
        table.add_row(str(idx), f"{base_command}{args}", description)

    table.add_row("0", "[bold red]Exit[/bold red]", "Exit the menu.")
    console.print(table)


def _get_user_choice(commands_keys: list):
    """Asks the user for their choice and validates it in a loop."""
    while True:
        try:
            choice_str = console.input(
                "\n[bold cyan]🎯 Select a command by number (or 0 to exit): [/bold cyan]"
            )
            choice = int(choice_str)
            if 0 <= choice <= len(commands_keys):
                return None if choice == 0 else commands_keys[choice - 1]
            else:
                console.print(
                    "[bold red]❌ Number out of range. Please try again.[/bold red]"
                )
        except (ValueError, IndexError):
            console.print(
                "[bold red]❌ Invalid input. Please enter a valid number.[/bold red]"
            )


def display_menu():
    """
    Affiche un menu propre et formaté en orchestrant des fonctions d'aide.
    """
    # 1. Get the user and display the appropriate welcome panel
    employee = get_current_user()
    _display_welcome_panel(employee)

    # 2. Get the relevant commands for the user
    commands_dict = _get_commands_for_user(employee)

    # 3. Build and display the command table
    _build_and_display_table(commands_dict)

    # 4. Get and validate the user's choice
    commands_keys = list(commands_dict.keys())
    return _get_user_choice(commands_keys)
