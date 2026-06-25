from datetime import datetime
from app.extensions import db


class AfterCare(db.Model):

    __tablename__ = "aftercares"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    
    service_id = db.Column(
        db.Integer,
        db.ForeignKey("services.id"),
        nullable=False,
        unique=True
    )

    content = db.Column(
        db.Text,
        nullable=False
    )

    is_active = db.Column(
        db.Boolean,
        default=True
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )