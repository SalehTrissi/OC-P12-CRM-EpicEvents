from sqlalchemy import (
    Column, Integer, Float, Boolean, DateTime, ForeignKey
)
from sqlalchemy.ext.declarative import declarative_base
from utils.validators import validate_positive_amount
from sqlalchemy.orm import relationship, validates
from datetime import datetime


Base = declarative_base()


class Contract(Base):
    __tablename__ = 'contracts'

    contract_id = Column(Integer, primary_key=True, autoincrement=True)
    total_amount = Column(Float, nullable=False)
    remaining_amount = Column(Float, nullable=False)
    date_created = Column(DateTime, default=datetime.timezone.utc)
    is_signed = Column(Boolean, default=False)

    client_id = Column(Integer, ForeignKey(
        'clients.client_id'), nullable=False)
    client = relationship('Client', back_populates='contracts')

    sales_contact_id = Column(Integer, ForeignKey(
        'employees.employee_id'), nullable=False)
    sales_contact = relationship('Employee', back_populates='contracts')

    # Relations
    events = relationship('Event', back_populates='contract')

    # Validation des champs
    @validates('total_amount', 'remaining_amount')
    def validate_amounts(self, key, value):
        return validate_positive_amount(value, key)

    # Méthode utilitaire
    @classmethod
    def get_unsigned_contracts(cls, session):
        """
        Retourne tous les contrats non signés.
        """
        return session.query(cls).filter_by(is_signed=False).all()

    def __repr__(self):
        status = "Signed" if self.is_signed else "Unsigned"
        return (f"<Contract {self.contract_id}: {status}, "
                f"Total: {self.total_amount}, Remaining:{self.remaining_amount}>")
