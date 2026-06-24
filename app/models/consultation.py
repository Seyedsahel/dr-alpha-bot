from datetime import datetime
from app.extensions import db


class Consultation(db.Model):

    __tablename__ = "consultations"

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
        nullable=True
    )

    note = db.Column(
        db.Text,
        nullable=True
    )

    status = db.Column(
        db.String(20),
        default="pending"
    )
    # pending -> called -> closed

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )