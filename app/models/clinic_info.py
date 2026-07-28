from datetime import datetime
from app.extensions import db


class ClinicInfo(db.Model):

    __tablename__ = "clinic_info"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    address = db.Column(
        db.Text,
        nullable=True
    )

    phone = db.Column(
        db.String(30),
        nullable=True
    )

    website = db.Column(
        db.String(200),
        nullable=True
    )

    instagram = db.Column(
        db.String(200),
        nullable=True
    )

    bale_channel = db.Column(
        db.String(200),
        nullable=True
    )

    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )