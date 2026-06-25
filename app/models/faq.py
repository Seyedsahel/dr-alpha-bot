from datetime import datetime
from app.extensions import db


class FAQ(db.Model):

    __tablename__ = "faqs"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    question = db.Column(
        db.Text,
        nullable=False
    )

    answer = db.Column(
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