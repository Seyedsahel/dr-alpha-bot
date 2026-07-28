from datetime import datetime
from app.extensions import db


class Doctor(db.Model):

    __tablename__ = "doctors"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(150),
        nullable=False
    )

    medical_license_number = db.Column(
        db.String(50),
        nullable=True
    )

    photo_path = db.Column(
        db.String(255),
        nullable=True
    )

    is_active = db.Column(
        db.Boolean,
        default=True
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )