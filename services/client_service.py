from EpicEventsCRM.utils.permissions import has_permission
from EpicEventsCRM.models.client_model import Client
from sqlalchemy.exc import IntegrityError
from db.database import SessionLocal
from auth import get_current_user


def create_client():
    """
    Creates a new client if the user has the necessary permissions.
    """
    current_user = get_current_user()
    if not current_user:
        print("You must be authenticated to create a client.")
        return

    if not has_permission(current_user, 'create_client'):
        print("You do not have permission to create a client.")
        return

    # Collecting customer information
    full_name = input("Full Name: ")
    email = input("Email: ")
    phone_number = input("Phone Number: ")
    company_name = input("Company Name: ")

    client = Client(
        full_name=full_name,
        email=email,
        phone_number=phone_number,
        company_name=company_name,
        sales_contact=current_user
    )

    # Save to database
    with SessionLocal as session:
        session.add(client)
        try:
            session.commit()
            print("Client created successfully.")
        except IntegrityError:
            session.rollback()
            print("Error: A customer with this email already exists.")
        except Exception as e:
            session.rollback()
            print(f"Error creating client: {e}")


def update_client(client_id):
    """
    Updates a client's information if the user has the necessary permissions.
    """
    current_user = get_current_user()
    if not current_user:
        print("You must be authenticated to modify a client.")
        return

    with SessionLocal as session:
        client = session.query(Client).filter_by(client_id=client_id).first()
        if not client:
            print("Client not found.")
            return

        # Check if the user has the right to modify this client
        if not has_permission(current_user, 'update_client'):
            print("You do not have permission to modify this client.")
            return

        # Collecting new information
        print("Leave blank to not modify the field.")
        full_name = input(f"Full name ({client.full_name}): ") or client.full_name
        email = input(f"Email ({client.email}): ") or client.email
        phone_number = input(
            f"Phone number ({client.phone_number}): ") or client.phone_number
        company_name = input(
            f"Company name ({client.company_name}): ") or client.company_name

        # Mise à jour du client
        client.full_name = full_name
        client.email = email
        client.phone_number = phone_number
        client.company_name = company_name

        # Save to database
        try:
            session.commit()
            print("Client updated successfully.")
        except IntegrityError:
            session.rollback()
            print("Error: A customer with this email already exists.")
        except Exception as e:
            session.rollback()
            print(f"Error updating client: {e}")
