from datetime import datetime
from app.extensions import db


class Service(db.Model):

    __tablename__ = "services"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(150),
        nullable=False,
        unique=True
    )

    price = db.Column(
        db.BigInteger,
        nullable=True
    )

    description = db.Column(
        db.Text,
        nullable=True
    )

    is_active = db.Column(
        db.Boolean,
        default=True
    )

    recovery_days = db.Column(
        db.Integer, 
        nullable=True
    )

    reminders = db.relationship(
        "Reminder",
        backref="service",
        lazy=True
    )

    aftercare = db.relationship(
        "AfterCare",
        backref="service",
        uselist=False
    )

    appointments = db.relationship(
        "Appointment",
        backref="service",
        lazy=True
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )