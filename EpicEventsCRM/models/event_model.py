from sqlalchemy import (
    Column, Integer, String, DateTime, ForeignKey
)
from sqlalchemy.ext.declarative import declarative_base
from utils.validators import validate_string_length
from sqlalchemy.orm import relationship, validates
from datetime import datetime


Base = declarative_base()


class Event(Base):
    __tablename__ = 'events'

    event_id = Column(Integer, primary_key=True, autoincrement=True)
    event_name = Column(String(100), nullable=False)
    event_start_date = Column(DateTime, nullable=False)
    event_end_date = Column(DateTime, nullable=False)
    location = Column(String(200), nullable=False)
    attendees = Column(Integer, nullable=False)
    notes = Column(String(1000))

    client_id = Column(Integer, ForeignKey('clients.client_id'), nullable=False)
    client = relationship('Client', back_populates='events')

    contract_id = Column(Integer, ForeignKey('contracts.contract_id'), nullable=False)
    contract = relationship('Contract', back_populates='events')

    support_contact_id = Column(Integer, ForeignKey(
        'employees.employee_id'), nullable=False)
    support_contact = relationship('Employee', back_populates='events')

    # Validation des champs
    @validates('event_name')
    def validate_event_name(self, key, value):
        return validate_string_length(value, key, 100)

    @validates('location')
    def validate_location(self, key, value):
        return validate_string_length(value, key, 200)

    @validates('attendees')
    def validate_attendees(self, key, value):
        if value < 0:
            raise ValueError("Le nombre de participants ne peut pas être négatif")
        return value

    # Méthode utilitaire
    @classmethod
    def get_upcoming_events_for_support(cls, session, support_employee_id):
        """
        Retourne les événements à venir pour un employé du support donné.
        """
        now = datetime.utcnow()
        return session.query(cls).filter(
            cls.support_contact_id == support_employee_id,
            cls.event_start_date >= now
        ).order_by(cls.event_start_date).all()

    def __repr__(self):
        return f"<Event {self.event_id}: {self.event_name} for {self.client.full_name}>"
