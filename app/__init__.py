from flask import Flask
from .extensions import db, migrate
from app.models import *
import os
from app.config import Config
from datetime import timedelta
from flask import request
from app.utils.jwt_auth import verify_token
from app.routes.admin import admin_auth_bp
from app.routes.uploads import uploads_bp

from flask_wtf import CSRFProtect
from app.routes.admin import (admin_slots_bp, admin_appointments_bp, admin_consultations_bp)
from app.routes.bot import bot_slots_bp
from app.routes.bot import appointments_bp
from app.routes.bot import consultations_bp
from app.routes.admin import admin_services_bp
from app.routes.bot import services_bp
from app.routes.bot import faqs_bp
from app.routes.admin import admin_aftercares_bp
from app.routes.bot import aftercares_bp
from app.routes.bot import festivals_bp
from app.routes.admin import admin_festivals_bp
from app.routes.bot import reminders_bp
from app.routes.admin import admin_reminders_bp
from app.routes.bot import users_bp
from app.routes.admin import admin_users_bp
from app.routes.admin_panel import admin_panel_bp
from app.routes.admin import admin_faqs_bp

from app.extensions import limiter


csrf = CSRFProtect()

def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///clinic.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["UPLOAD_FOLDER"] = "/srv/dr-alpha/uploads"
    app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024
    app.config.from_object(Config)

   
   
    csrf.init_app(app)
    csrf.exempt(admin_auth_bp)
    csrf.exempt(uploads_bp)
    csrf.exempt(admin_slots_bp)
    csrf.exempt(admin_appointments_bp)
    csrf.exempt(admin_consultations_bp)
    csrf.exempt(admin_services_bp)
    csrf.exempt(admin_faqs_bp)
    csrf.exempt(admin_aftercares_bp)
    csrf.exempt(admin_festivals_bp)
    csrf.exempt(admin_reminders_bp)
    csrf.exempt(admin_users_bp)
    csrf.exempt(admin_panel_bp)
    csrf.exempt(bot_slots_bp)
    csrf.exempt(appointments_bp)
    csrf.exempt(consultations_bp)
    csrf.exempt(services_bp)
    csrf.exempt(faqs_bp)
    csrf.exempt(aftercares_bp)
    csrf.exempt(festivals_bp)   
    csrf.exempt(reminders_bp)
    csrf.exempt(users_bp)

    os.makedirs(
        os.path.join(
            app.config["UPLOAD_FOLDER"],
            "festivals"
        ), exist_ok=True
    )

    db.init_app(app)
    migrate.init_app(app, db)
    limiter.init_app(app)

    app.register_blueprint(
        admin_auth_bp,
        url_prefix="/api/admin"
    )


    ADMIN_API_EXEMPT_PATHS = {
        "/api/admin/login"
    }

    @app.before_request
    def protect_admin_api():
        if not request.path.startswith("/api/admin"):
            return None
        
        if request.path in ADMIN_API_EXEMPT_PATHS:
            return None
        
        auth_header = request.headers.get("Authorization", "")

        if not auth_header.startswith("Bearer "):
            return {"error": "توکن ارسال نشده است"}, 401
        
        token = auth_header.split(" ",1)[1]
        
        payload = verify_token(token)

        if not payload:
            return {"error": "توکن نامعتبر یا منقضی شده است"}, 401

        return None
    
    app.config.update(
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE="Lax",
        SESSION_COOKIE_SECURE=False,
        PERMANENT_SESSION_LIFETIME=timedelta(hours=8)
    )


    app.register_blueprint(uploads_bp)

    app.register_blueprint(
        admin_slots_bp,
        url_prefix="/api/admin")
    
    app.register_blueprint(
        admin_appointments_bp,
        url_prefix="/api/admin")
    
    app.register_blueprint(
        admin_consultations_bp,
        url_prefix="/api/admin")

    
    app.register_blueprint(
        bot_slots_bp,
        url_prefix="/api"
    )

    app.register_blueprint(
        appointments_bp,
        url_prefix="/api")
    
    app.register_blueprint(
        consultations_bp,
        url_prefix="/api"
    )

    app.register_blueprint(
        admin_services_bp,
        url_prefix="/api/admin"
    )

    app.register_blueprint(
        services_bp,
        url_prefix="/api"
    )

    
    app.register_blueprint(
        admin_faqs_bp,
        url_prefix="/api/admin")

    app.register_blueprint(
        faqs_bp,
        url_prefix="/api"
    )
    
    app.register_blueprint(
        admin_aftercares_bp,
        url_prefix="/api/admin"
    )
    app.register_blueprint(
        aftercares_bp,
        url_prefix="/api"
    )

    app.register_blueprint(
        festivals_bp,
        url_prefix="/api"
    )

    app.register_blueprint(
        admin_festivals_bp,
        url_prefix="/api/admin"
    )

    app.register_blueprint(
        reminders_bp,
        url_prefix="/api"
    )

    app.register_blueprint(
        admin_reminders_bp,
        url_prefix="/api/admin" 
    )

    app.register_blueprint(
        users_bp,
        url_prefix="/api"
    )

    app.register_blueprint(
        admin_users_bp,
        url_prefix="/api/admin"
    )

        
    # پنل مدیریت (Jinja2)
    app.register_blueprint(
        admin_panel_bp,
        url_prefix="/admin/panel"
    )

    # فیلتر jalali برای Jinja
    from app.utils.jalali import gregorian_to_jalali_str
    app.jinja_env.filters["jalali"] = gregorian_to_jalali_str

    
    
    
    return app