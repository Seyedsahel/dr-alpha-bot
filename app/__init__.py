from flask import Flask
from .extensions import db, migrate
from app.models import *

def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///clinic.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    migrate.init_app(app, db)

    from app.routes.admin import (admin_slots_bp, admin_appointments_bp)
    app.register_blueprint(
        admin_slots_bp,
        url_prefix="/api/admin")
    
    app.register_blueprint(
        admin_appointments_bp,
        url_prefix="/api/admin")
    
    from app.routes.bot import bot_slots_bp
    app.register_blueprint(
        bot_slots_bp,
        url_prefix="/api"
    )

    from app.routes.bot import appointments_bp
    app.register_blueprint(
        appointments_bp,
        url_prefix="/api")


    return app