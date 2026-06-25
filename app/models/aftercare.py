from datetime import datetime
from app.extensions import db


class AfterCare(db.Model):

    __tablename__ = "aftercares"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    service_name = db.Column(
        db.String(150),
        nullable=False
    )

    content = db.Column(
        db.Text,
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )