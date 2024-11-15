from EpicEventsCRM.models.employee_model import Employee, DepartmentEnum
from sqlalchemy.exc import IntegrityError
from db.database import SessionLocal
from getpass import getpass


def main():
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


main()
