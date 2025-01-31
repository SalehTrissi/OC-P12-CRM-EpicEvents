from .commands_registry import get_command_list
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box


console = Console()


def help_command():
    """
    Display a list of all available commands with their descriptions.
    These commands are defined in commands_registry.py.
    """
    console.print(
        Panel("[bold cyan]Available Commands:[/bold cyan]",
              box=box.ROUNDED, style="bold green")
    )

    commands = get_command_list()

    # Create a table for commands
    table = Table(
        title="[bold magenta]Command Help[/bold magenta]",
        box=box.ROUNDED,
        header_style="bold white"
    )
    table.add_column("Command", justify="left", style="cyan")
    table.add_column("Description", justify="left", style="green")

    for command, description in commands.items():
        table.add_row(f"[bold cyan]{command}[/bold cyan]", description)

    console.print(table, justify="center")
