from datetime import datetime
from app.extensions import db


class Reminder(db.Model):

    __tablename__ = "reminders"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    service = db.Column(
        db.String(150),
        nullable=False
    )

    procedure_date = db.Column(
        db.Date,
        nullable=False
    )

    reminder_date = db.Column(
        db.Date,
        nullable=False
    )

    sent = db.Column(
        db.Boolean,
        default=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )