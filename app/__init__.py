from flask import Flask
from .extensions import db, migrate
from app.models import *
import os
from app.config import Config
def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///clinic.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["UPLOAD_FOLDER"] = os.path.join(
        app.root_path,
        "uploads")
    app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024
    app.config.from_object(Config)

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

    from app.routes.bot import reminders_bp
    app.register_blueprint(
        reminders_bp,
        url_prefix="/api"
    )

    from app.routes.admin import admin_reminders_bp
    app.register_blueprint(
        admin_reminders_bp,
        url_prefix="/api/admin" 
    )

    from app.routes.bot import users_bp
    app.register_blueprint(
        users_bp,
        url_prefix="/api"
    )

    from app.routes.admin import admin_users_bp
    app.register_blueprint(
        admin_users_bp,
        url_prefix="/api/admin"
    )

        
    # پنل مدیریت (Jinja2)
    from app.routes.admin_panel import admin_panel_bp
    app.register_blueprint(
        admin_panel_bp,
        url_prefix="/admin/panel"
    )

    # فیلتر jalali برای Jinja
    from app.utils.jalali import gregorian_to_jalali_str
    app.jinja_env.filters["jalali"] = gregorian_to_jalali_str

    
    
    
    return app