from datetime import datetime
from app.extensions import db

class User(db.Model):
    __tablename__ = "users"
    
    id = db.Column(db.Integer, primary_key=True)
    
    chat_id = db.Column(
        db.String(100), unique=True,
        nullable=False)
    
    first_name = db.Column(
        db.String(100),
        nullable=False)
    
    last_name = db.Column(
        db.String(100),
        nullable=True)
    
    phone = db.Column(
        db.String(20),
        nullable=True)  
    
    is_admin = db.Column(
        db.Boolean,
        default=False)  
    
    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow)
    
    appointments = db.relationship(
        "Appointment",
        backref="user",
        lazy=True)