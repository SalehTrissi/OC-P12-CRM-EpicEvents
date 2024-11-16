from EpicEventsCRM.utils.permissions import has_permission
from EpicEventsCRM.utils.validators import validate_positive_amount
from EpicEventsCRM.models.contract_model import Contract
from EpicEventsCRM.models.client_model import Client
from db.database import SessionLocal
from auth import get_current_user


def create_contract():
    """
    Creates a new contract if the user has the necessary permissions.
    """
    current_user = get_current_user()
    if not current_user:
        print("You must be authenticated to create a contract.")
        return
    if not has_permission(current_user, 'create_contract'):
        print("You do not have permission to create a contract.")
        return

    with SessionLocal as session:
        # Customer selection
        client_id_input = input("Customer ID : ")

        try:
            client_id = int(client_id_input)
        except ValueError:
            print("Invalid client ID.")
            return

        client = session.query(Client).filter_by(client_id=client_id).first()
        if not client:
            print("Client not found.")
            return

        # Collecting contract information
        try:
            total_amount = float(input("Total amount: "))
            total_amount = validate_positive_amount(total_amount, 'total_amount')
        except ValueError as ve:
            print(f"Validation error: {ve}")
            return

        try:
            remaining_amount = float(input("Remaining amount: "))
            remaining_amount = validate_positive_amount(
                remaining_amount, 'remaining_amount')
        except ValueError as ve:
            print(f"Validation error: {ve}")
            return

        if remaining_amount > total_amount:
            print("The remaining amount cannot be greater than the total amount.")
            return

        is_signed_input = input("Contract signed? (Y/N): ").upper()
        is_signed = True if is_signed_input == "y" else False

        # Contract creation
        contract = Contract(
            total_amount=total_amount,
            remaining_amount=remaining_amount,
            is_signed=is_signed,
            client=client,
            sales_contact=current_user
        )

        # Save to database
        with SessionLocal as session:
            session.add(contract)
            try:
                session.commit()
                print("Contract created successfully.")
            except Exception as e:
                session.rollback()
                print(f"Error creating contract: {e}")


def update_contract(contract_id):
    """
    Updates the information of a contract if the user has the necessary permissions.
    """
    current_user = get_current_user()
    if not current_user:
        print("You must be authenticated to modify a contract.")
        return

    if not has_permission(current_user, 'modify_contract'):
        print("Vous n'avez pas la permission de modifier un contrat.")
        return

    with SessionLocal as session:
        try:
            contract_id = int(contract_id)
        except ValueError:
            print("Invalid contract ID.")
            return

        contract = session.query(Contract).filter_by(contract_id=contract_id).first()
        if not contract:
            print("Contract not found.")
            return

        # Check if the user has the right to modify this contract
        if not has_permission(current_user, 'modify_contract'):
            print("You do not have permission to modify this contract.")
            return

        # Collecting new information
        print("Leave blank to not modify the field.")
        total_amount_input = input(f"Total amount ({contract.total_amount}): ")
        if total_amount_input:
            try:
                total_amount = float(total_amount_input)
                total_amount = validate_positive_amount(total_amount, 'total_amount')
            except ValueError as ve:
                print(f"Validation error: {ve}")
                return
        else:
            total_amount = contract.total_amount

        remaining_amount_input = input(
            f"Remaining amount ({contract.remaining_amount}): ")
        if remaining_amount_input:
            try:
                remaining_amount = float(remaining_amount_input)
                remaining_amount = validate_positive_amount(
                    remaining_amount, 'remaining_amount')
            except Exception as ve:
                print(f"Validation error: {ve}")
                return
        else:
            remaining_amount = contract.remaining_amount

        if remaining_amount > total_amount:
            print("The remaining amount cannot be greater than the total amount.")
            return

        is_signed_input = input(
            f"Signed contract ({'Y' if contract.is_signed else 'N'}) ? (Y/N): ").upper()
        if is_signed_input == 'Y':
            is_signed = True
        elif is_signed_input == 'N':
            is_signed = False
        else:
            is_signed = contract.is_signed

        # Contract update
        contract.total_amount = total_amount
        contract.remaining_amount = remaining_amount
        contract.is_signed = is_signed

        # Save to database
        try:
            session.commit()
            print("Contrat mis à jour avec succès.")
        except Exception as e:
            session.rollback()
            print(f"Error updating contract: {e}")
