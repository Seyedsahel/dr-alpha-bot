from flask import Blueprint, request, current_app

from app.utils.jwt_auth import generate_token

from app.extensions import limiter

admin_auth_bp = Blueprint(
    "admin_auth",
    __name__
)


@admin_auth_bp.route(
    "/login",
    methods=["POST"]
)

@limiter.limit("5 per minute")

def admin_login():

    data = request.get_json() or {}

    username = data.get("username")
    password = data.get("password")

    if (
        username == current_app.config["ADMIN_USERNAME"]
        and password == current_app.config["ADMIN_PASSWORD"]
    ):
        token = generate_token(username)

        return {
            "token": token
        }, 200

    return {
        "error": "نام کاربری یا رمز عبور اشتباه است"
    }, 401