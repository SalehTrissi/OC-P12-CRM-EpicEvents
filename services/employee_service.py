from EpicEventsCRM.models.employee_model import Employee, DepartmentEnum
from EpicEventsCRM.utils.permissions import has_permission
from sqlalchemy.exc import IntegrityError
from db.database import SessionLocal
from auth import get_current_user
from getpass import getpass


def create_employee():
    """
    Creates a new employee if the user has the necessary permissions.
    """
    current_user = get_current_user()
    if not current_user:
        print("You must be authenticated to create an employee.")
        return

    if not has_permission(current_user, 'manage_users'):
        print("You do not have permission to create an employee.")
        return

    # Collect employee information
    first_name = input("First name: ")
    last_name = input("Last name: ")
    email = input("Email: ")
    phone_number = input("Phone number: ")
    department_input = input("Department (COMMERCIAL/SUPPORT/MANAGEMENT): ").upper()
    password = getpass("Password: ")

    # Verify department
    if department_input not in DepartmentEnum.__members__:
        print("Invalid department. Please choose from COMMERCIAL, SUPPORT or MANAGEMENT.")
        return

    department = DepartmentEnum[department_input]

    # Create employee
    employee = Employee(
        first_name=first_name,
        last_name=last_name,
        email=email,
        phone_number=phone_number,
        department=department
    )
    employee.set_password(password)

    # Save to database
    with SessionLocal as session:
        session.add(employee)
        try:
            session.commit()
            print("Employee created successfully.")
        except IntegrityError:
            session.rollback()
            print("Error: An employee with this email already exists.")
        except Exception as e:
            session.rollback()
            print(f"Error creating employee: {e}")


def update_employee(employee_id):
    """
    Updates an employee's information if the user has the necessary permissions.
    """
    current_user = get_current_user()
    if not current_user:
        print("You must be authenticated to edit an employee.")
        return

    if not has_permission(current_user, 'manage_users'):
        print("You do not have permission to edit an employee.")
        return

    with SessionLocal as session:
        employee = session.query(Employee).filter_by(employee_id=employee_id).first()
        if not employee:
            print("Employee not found.")
            return

        # Collecting new information
        print("Leave blank to not modify the field.")
        first_name = input(
            f"First name ({employee.first_name}): ") or employee.first_name
        last_name = input(f"Name ({employee.last_name}): ") or employee.last_name
        email = input(f"Email ({employee.email}): ") or employee.email
        phone_number = input(
            f"Phone number ({employee.phone_number}): ") or employee.phone_number
        department_input = input(
            f"Department ({employee.department.name}): ").upper() or employee.department.name

        if department_input not in DepartmentEnum.__members__:
            print("Invalid department. Please choose from COMMERCIAL, SUPPORT or MANAGEMENT.")
            return

        department = DepartmentEnum[department_input]

        # Update employee
        employee.first_name = first_name
        employee.last_name = last_name
        employee.email = email
        employee.phone_number = phone_number
        employee.department = department

        # Update password
        change_password = input("Do you want to change password? (Y/N) : ").upper()
        if change_password == 'O':
            password = getpass("New password: ")
            employee.set_password(password)

        # Save to database
        try:
            session.commit()
            print("Employee successfully updated.")
        except IntegrityError:
            session.rollback()
            print("Error: An employee with this email already exists.")
        except Exception as e:
            session.rollback()
            print(f"Error updating employee: {e}")
