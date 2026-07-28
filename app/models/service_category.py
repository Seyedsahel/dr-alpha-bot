from datetime import datetime
from app.extensions import db


class ServiceCategory(db.Model):

    __tablename__ = "service_categories"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(150),
        nullable=False,
        unique=True
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )