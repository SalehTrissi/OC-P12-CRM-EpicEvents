from sqlalchemy import Column, String, Integer, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, validates
from ..utils.validators import validate_email, validate_phone_number, validate_string_length
import enum


Base = declarative_base()


class DepartmentEnum(enum.Enum):
    COMMERCIAL = 'Commercial'
    SUPPORT = 'Support'
    MANAGEMENT = 'Management'


class Employee(Base):
    __tablename__ = 'employees'

    employee_id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    phone_number = Column(String(20), nullable=False)
    department = Column(Enum(DepartmentEnum), nullable=False)

    # Relations
    clients = relationship('Client', back_populates='sales_contact')
    contracts = relationship('Contract', back_populates='sales_contact')
    events = relationship('Event', back_populates='support_contact')

    # Validation des champs
    @validates('email')
    def validate_email_address(self, key, address):
        return validate_email(address)

    @validates('first_name', 'last_name')
    def validate_name_length(self, key, value):
        return validate_string_length(value, key, 50)

    @validates('phone_number')
    def validate_phone(self, key, number):
        return validate_phone_number(number)

    def __repr__(self):
        return f"<Employee {self.employee_id}: {self.first_name} {self.last_name} ({self.department.value})>"
