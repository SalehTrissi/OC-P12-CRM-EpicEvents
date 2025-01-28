from EpicEventsCRM.utils.validators import validate_positive_amount
from EpicEventsCRM.utils.permissions import has_permission
from EpicEventsCRM.models.contract_model import Contract
from EpicEventsCRM.models.client_model import Client
from db.database import SessionLocal
from auth import get_current_user
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from rich import box
import sentry_sdk


console = Console()


def create_contract():
    """
    Creates a new contract with a user-friendly and visually appealing interface.
    """
    current_user = get_current_user()
    if not current_user:
        console.print(
            Panel("[bold red]You must be authenticated to create a contract."
                  "[/bold red]", box=box.ROUNDED))
        return

    if not has_permission(current_user, 'create_contract'):
        console.print(
            Panel("[bold red]You do not have permission to create a contract."
                  "[/bold red]", box=box.ROUNDED))
        return

    console.print(Panel("[bold cyan]Create New Contract[/bold cyan]",
                        box=box.ROUNDED, style="bold green"))

    # Select client
    client_id_input = Prompt.ask("[bold yellow]Enter Client ID[/bold yellow]")
    try:
        client_id = int(client_id_input)
    except ValueError as e:
        console.print(Panel("[bold red]Invalid Client ID.[/bold red]", box=box.ROUNDED))
        sentry_sdk.capture_exception(e)
        return

    with SessionLocal as session:
        client = session.query(Client).filter_by(client_id=client_id).first()
        if not client:
            console.print(
                Panel("[bold red]Client not found.[/bold red]", box=box.ROUNDED))
            sentry_sdk.capture_message(
                f"Client with ID {client_id} not found.", level="error")
            return

        # Collect contract information
        try:
            total_amount = float(Prompt.ask(
                "[bold yellow]Enter total amount[/bold yellow]"))
            total_amount = validate_positive_amount(total_amount, 'total_amount')
        except ValueError as ve:
            console.print(Panel(f"[bold red]Validation error: {
                          ve}[/bold red]", box=box.ROUNDED))
            sentry_sdk.capture_exception(ve)
            return

        try:
            remaining_amount = float(Prompt.ask(
                "[bold yellow]Enter remaining amount[/bold yellow]"))
            remaining_amount = validate_positive_amount(
                remaining_amount, 'remaining_amount')
        except ValueError as ve:
            console.print(Panel(f"[bold red]Validation error: {
                          ve}[/bold red]", box=box.ROUNDED))
            sentry_sdk.capture_exception(ve)
            return

        if remaining_amount > total_amount:
            console.print(Panel("[bold red]The remaining amount cannot be greater"
                                " than the total amount.[/bold red]", box=box.ROUNDED))
            sentry_sdk.capture_message(
                "Remaining amount cannot be greater than total amount.", level="warning")
            return

        is_signed_input = Prompt.ask(
            "[bold yellow]Is the contract signed? (Y/N)[/bold yellow]",
            default="N").upper()
        is_signed = is_signed_input == "Y"

        # Create contract
        contract = Contract(
            total_amount=total_amount,
            remaining_amount=remaining_amount,
            is_signed=is_signed,
            client=client,
            sales_contact=current_user
        )

        # Save to database
        session.add(contract)
        try:
            session.commit()
            console.print(
                Panel("[bold green]Contract created successfully![/bold green]",
                      box=box.ROUNDED))
            sentry_sdk.capture_message(
                f"Contract for Client ID {client_id} created successfully.",
                level="info"
            )
        except Exception as e:
            session.rollback()
            console.print(Panel(f"[bold red]Error creating contract: {
                          e}[/bold red]", box=box.ROUNDED))
            sentry_sdk.capture_exception(e)


def update_contract(contract_id):
    """
    Updates a contract with a user-friendly and visually appealing interface.
    """
    current_user = get_current_user()
    if not current_user:
        console.print(
            Panel("[bold red]You must be authenticated to update a contract."
                  "[/bold red]", box=box.ROUNDED))
        return

    if not has_permission(current_user, 'modify_contract'):
        console.print(
            Panel("[bold red]You do not have permission to modify a contract."
                  "[/bold red]", box=box.ROUNDED))
        return

    with SessionLocal as session:
        try:
            contract_id = int(contract_id)
        except ValueError as e:
            console.print(
                Panel("[bold red]Invalid Contract ID.[/bold red]", box=box.ROUNDED))
            sentry_sdk.capture_exception(e)
            return

        contract = session.query(Contract).filter_by(contract_id=contract_id).first()
        if not contract:
            console.print(
                Panel("[bold red]Contract not found.[/bold red]", box=box.ROUNDED))
            sentry_sdk.capture_message(
                f"Contract with ID {contract_id} not found.", level="error")
            return

        console.print(Panel(f"[bold cyan]Update Contract: {contract.contract_id}"
                            "[/bold cyan]", box=box.ROUNDED, style="bold green"))

        console.print(
            "[bold yellow](Leave blank to keep the current value.)[/bold yellow]\n")

        # Collecting new information
        total_amount_input = Prompt.ask(
            f"[bold yellow]Total amount[/bold yellow] [bold green](current: {
                contract.total_amount})[/bold green]",
            default=str(contract.total_amount),
            show_default=False
        )
        try:
            total_amount = float(total_amount_input)
            total_amount = validate_positive_amount(total_amount, 'total_amount')
        except ValueError as ve:
            console.print(Panel(f"[bold red]Validation error: {
                          ve}[/bold red]", box=box.ROUNDED))
            sentry_sdk.capture_exception(ve)
            return

        remaining_amount_input = Prompt.ask(
            f"[bold yellow]Remaining amount[/bold yellow] [bold green](current: {
                contract.remaining_amount})[/bold green]",
            default=str(contract.remaining_amount),
            show_default=False
        )
        try:
            remaining_amount = float(remaining_amount_input)
            remaining_amount = validate_positive_amount(
                remaining_amount, 'remaining_amount')
        except ValueError as ve:
            console.print(Panel(f"[bold red]Validation error: {
                          ve}[/bold red]", box=box.ROUNDED))
            sentry_sdk.capture_exception(ve)
            return

        if remaining_amount > total_amount:
            console.print(Panel("[bold red]The remaining amount cannot be greater"
                                " than the total amount.[/bold red]", box=box.ROUNDED))
            sentry_sdk.capture_message(
                "Remaining amount cannot be greater than total amount.", level="warning")
            return

        is_signed_input = Prompt.ask(
            f"[bold yellow]Signed contract[/bold yellow] [bold green](current: {
                'Y' if contract.is_signed else 'N'})[/bold green]",
            default="Y" if contract.is_signed else "N",
            show_default=False
        ).upper()
        is_signed = is_signed_input == "Y"

        # Update contract
        contract.total_amount = total_amount
        contract.remaining_amount = remaining_amount
        contract.is_signed = is_signed

        # Save to database
        try:
            session.commit()
            console.print(
                Panel("[bold green]Contract updated successfully!"
                      "[/bold green]", box=box.ROUNDED))
            sentry_sdk.capture_message(
                f"Contract ID {contract_id} updated successfully.", level="info"
            )
        except Exception as e:
            session.rollback()
            console.print(Panel(f"[bold red]Error updating contract: {
                          e}[/bold red]", box=box.ROUNDED))
            sentry_sdk.capture_exception(e)
