from config import JWT_SECRET, JWT_ALGORITHM, JWT_EXP_DELTA_SECONDS
from EpicEventsCRM.utils.permissions import has_permission
from EpicEventsCRM.models.employee_model import Employee
from datetime import datetime, timedelta, timezone
from db.database import SessionLocal
from sqlalchemy.orm import Session
from getpass import getpass
import jwt
import os


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
    Handles the user login process.
    """
    email = input("Email: ").strip().lower()
    password = getpass("Password: ")

    # Create a session to access the database
    with SessionLocal as session:
        token = authenticate(session, email, password)
    if token:
        save_token(token)
        print("Authentication successful.")
    else:
        print("Authentication failed.")


def logout():
    """
    Manages the user logout process.
    """
    delete_token()
    print("You are logged out.")


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
