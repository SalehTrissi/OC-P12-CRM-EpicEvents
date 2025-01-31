from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box
from EpicEventsCRM.utils.permissions import get_available_commands
from auth import get_current_user

console = Console()


def display_menu():
    """
    Display the menu once and return the command the user selected.
    If the user selects 0, return None.
    """
    employee = get_current_user()

    if not employee:
        panel = Panel(
            "[bold cyan]Welcome to Epic Events CRM[/bold cyan]\n"
            "[bold yellow]You are not logged in.[/bold yellow]\n"
            "[bold green]Please log in to access more commands.[/bold green]",
            box=box.DOUBLE,
            style="bold green",
            expand=True,
        )
        console.print(panel, justify="center")

        # Commands available for users who are not logged in
        commands_dict = {
            "menu": "Display the main menu again.",
            "login": "Log in to the system.",
            "help": "Display help for commands.",
        }
    else:
        panel = Panel(
            f"[bold cyan]Welcome, {employee.first_name}[/bold cyan] "
            f"[bold green]({employee.department.value})[/bold green]",
            box=box.HEAVY,
            style="bold green",
            expand=True
        )
        console.print(panel, justify="center")

        # Commands available based on user permissions
        commands_list = get_available_commands(employee)
        commands_dict = dict(commands_list)

    console.print("\n")

    # Prepare the table
    table = Table(
        title="[bold magenta]📜 Available Commands[/bold magenta]",
        box=box.SQUARE_DOUBLE_HEAD,
        header_style="bold magenta",
        expand=True
    )

    table.add_column("📌 Number", justify="center", style="bold yellow", no_wrap=True)
    table.add_column("🔹 Command", justify="center", style="bold cyan", no_wrap=True)
    table.add_column("📖 Description", justify="center", style="bold green")

    commands_keys = list(commands_dict.keys())
    for idx, command in enumerate(commands_keys, start=1):
        table.add_row(f"[bold yellow]{idx}[/bold yellow]", f"[bold cyan]{
                      command}[/bold cyan]", f"[green]{commands_dict[command]}[/green]")

    table.add_row("[bold yellow]0[/bold yellow]",
                  "[bold red]Exit[/bold red]", "[bold red]Exit the menu.[/bold red]")

    console.print(table)

    try:
        choice = int(console.input(
            "\n[bold cyan]🎯 Select a command by number (or 0 to exit): [/bold cyan]"))
    except ValueError:
        console.print(
            "[bold red]❌ Invalid input. Please enter a valid number.[/bold red]")
        return display_menu()

    return None if choice == 0 else commands_keys[choice - 1]
