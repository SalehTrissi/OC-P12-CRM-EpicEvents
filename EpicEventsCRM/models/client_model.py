from utils.validators import validate_email, validate_string_length, validate_phone_number
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, validates
from datetime import datetime

Base = declarative_base()


class Client(Base):
    __tablename__ = 'clients'

    client_id = Column(Integer, primary_key=True, autoincrement=True)
    full_name = Column(String(100), nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    phone_number = Column(String(20), nullable=False)
    company_name = Column(String(100), nullable=False)
    date_created = Column(DateTime, default=datetime.timezone.utc)
    last_contact_date = Column(DateTime, default=datetime.timezone.utc)

    sales_contact_id = Column(Integer, ForeignKey(
        'employees.employee_id'), nullable=False)
    sales_contact = relationship('Employee', back_populates='clients')

    # Relations
    contracts = relationship('Contract', back_populates='client')
    events = relationship('Event', back_populates='client')

    # Validation des champs
    @validates('email')
    def validate_email_address(self, key, address):
        return validate_email(address)

    @validates('full_name')
    def validate_full_name(self, key, value):
        return validate_string_length(value, key, 100)

    @validates('company_name')
    def validate_company_name(self, key, value):
        return validate_string_length(value, key, 100)

    @validates('phone_number')
    def validate_phone(self, key, number):
        return validate_phone_number(number)

    def __repr__(self):
        return f"<Client {self.client_id}: {self.full_name} from {self.company_name}>"


# Mise à jour automatique de last_contact_date
@event.listens_for(Client, 'before_update')
def receive_before_update(mapper, connection, target):
    target.last_contact_date = datetime.timezone.utc