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

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )