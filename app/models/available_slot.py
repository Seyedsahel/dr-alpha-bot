from datetime import datetime
from app.extensions import db


class AvailableSlot(db.Model):

    __tablename__ = "available_slots"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    start_time = db.Column(
        db.DateTime,
        nullable=False
    )

    is_booked = db.Column(
        db.Boolean,
        default=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    appointment = db.relationship(
        "Appointment",
        backref="slot",
        uselist=False) #one to one