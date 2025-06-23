from EpicEventsCRM.utils.permissions import get_available_commands
from auth import get_current_user
from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table
from rich.panel import Panel
from rich import box
import click
import sys

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


def _get_user_choice(commands_keys: list) -> tuple:
    """
    Asks the user for their choice and validates it in a loop.
    Returns a tuple of (command_string, list_of_arguments).
    """
    while True:
        try:
            choice_str = console.input(
                "\n[bold cyan]🎯 Select a command by number (or 0 to exit): [/bold cyan]"
            )
            choice = int(choice_str)

            if choice == 0:
                console.print("[bold red]👋 Exiting CRM... Goodbye![/bold red]")
                sys.exit(0)

            if 1 <= choice <= len(commands_keys):
                command_string = commands_keys[choice - 1]
                parts = command_string.split(" ")
                base_command = parts[0]
                execution_args = [base_command]

                if len(parts) > 1:
                    for arg_placeholder in parts[1:]:
                        prompt_text = arg_placeholder.replace(
                            '<', '').replace('>', '').replace('_', ' ').title()
                        user_input = Prompt.ask(
                            f"[bold yellow]Please enter {prompt_text}[/bold yellow]")
                        execution_args.append(user_input)

                return base_command, execution_args
            else:
                console.print(
                    "[bold red]❌ Number out of range. Please try again.[/bold red]")
        except (ValueError, IndexError):
            console.print(
                "[bold red]❌ Invalid input. Please enter a valid number.[/bold red]")


def run_menu_loop(cli_runner: click.Group):
    """
    This is the main public function that runs the interactive menu loop.
    It orchestrates the display, command retrieval, and execution.
    """
    while True:
        # 1. Get user and display welcome panel
        employee = get_current_user()
        _display_welcome_panel(employee)

        # 2. Get and display the table of available commands
        commands_dict = _get_commands_for_user(employee)
        _build_and_display_table(commands_dict)

        # 3. Get user's command choice and any required arguments
        base_command, execution_args = _get_user_choice(list(commands_dict.keys()))

        # 4. Execute the command
        if base_command == "menu":
            continue

        try:
            cli_runner.main(args=execution_args, standalone_mode=False)
            if base_command not in ["logout", "exit"]:
                console.input(
                    "\n[bold cyan]Press ENTER to return to the menu...[/bold cyan]")
        except SystemExit:
            console.input(
                "\n[bold cyan]Press ENTER to return to the menu...[/bold cyan]")
        except Exception as e:
            console.print(f"[bold red]An error occurred: {str(e)}[/bold red]")
            console.input(
                "\n[bold cyan]Press ENTER to return to the menu...[/bold cyan]")
