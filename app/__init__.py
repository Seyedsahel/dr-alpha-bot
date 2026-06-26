from flask import Flask
from .extensions import db, migrate
from app.models import *
import os

def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///clinic.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["UPLOAD_FOLDER"] = os.path.join(
        app.root_path,
        "uploads")
    app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024

    os.makedirs(
        os.path.join(
            app.config["UPLOAD_FOLDER"],
            "festivals"
        ), exist_ok=True
    )

    db.init_app(app)
    migrate.init_app(app, db)

    from app.routes.uploads import uploads_bp
    app.register_blueprint(uploads_bp)

    from app.routes.admin import (admin_slots_bp, admin_appointments_bp, admin_consultations_bp)
    app.register_blueprint(
        admin_slots_bp,
        url_prefix="/api/admin")
    
    app.register_blueprint(
        admin_appointments_bp,
        url_prefix="/api/admin")
    
    app.register_blueprint(
        admin_consultations_bp,
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
    
    from app.routes.bot import consultations_bp
    app.register_blueprint(
        consultations_bp,
        url_prefix="/api"
    )

    from app.routes.admin import admin_services_bp
    app.register_blueprint(
        admin_services_bp,
        url_prefix="/api/admin"
    )

    from app.routes.bot import services_bp
    app.register_blueprint(
        services_bp,
        url_prefix="/api"
    )

    from app.routes.admin import admin_faqs_bp
    app.register_blueprint(
        admin_faqs_bp,
        url_prefix="/api/admin")

    from app.routes.bot import faqs_bp
    app.register_blueprint(
        faqs_bp,
        url_prefix="/api"
    )
    
    from app.routes.admin import admin_aftercares_bp
    app.register_blueprint(
        admin_aftercares_bp,
        url_prefix="/api/admin"
    )
    from app.routes.bot import aftercares_bp
    app.register_blueprint(
        aftercares_bp,
        url_prefix="/api"
    )

    from app.routes.bot import festivals_bp
    app.register_blueprint(
        festivals_bp,
        url_prefix="/api"
    )

    from app.routes.admin import admin_festivals_bp
    app.register_blueprint(
        admin_festivals_bp,
        url_prefix="/api/admin"
    )
    

    return app