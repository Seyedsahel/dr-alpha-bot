from flask import Blueprint, request
from app.extensions import db
from app.models.user import User

users_bp = Blueprint(
    "users",
    __name__
)


@users_bp.route(
    "/users",
    methods=["POST"]
)
def create_or_get_user():

    data = request.get_json()

    chat_id = data.get("chat_id")
    first_name = data.get("first_name")
    last_name = data.get("last_name")
    phone = data.get("phone")

    if not chat_id or not first_name:
        return {
            "error": "chat_id and first_name are required"
        }, 400

    user = User.query.filter_by(
        chat_id=chat_id
    ).first()

    if user:

        user.first_name = first_name
        user.last_name = last_name

        if phone:
            user.phone = phone

        db.session.commit()

        return {
            "id": user.id,
            "chat_id": user.chat_id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "phone": user.phone,
            "menu_version": user.menu_version
        }, 200

    user = User(
        chat_id=chat_id,
        first_name=first_name,
        last_name=last_name,
        phone=phone
    )

    db.session.add(user)
    db.session.commit()

    return {
        "id": user.id,
        "chat_id": user.chat_id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "phone": user.phone,
        "menu_version": user.menu_version
    }, 201


@users_bp.route(
    "/users/chat/<chat_id>",
    methods=["GET"]
)
def get_user(chat_id):

    user = User.query.filter_by(
        chat_id=chat_id
    ).first()

    if not user:
        return {
            "error": "user not found"
        }, 404

    return {
        "id": user.id,
        "chat_id": user.chat_id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "phone": user.phone,
        "menu_version": user.menu_version
    }, 200

@users_bp.route(
    "/users/admins",
    methods=["GET"]
)
def get_admin_chat_ids():

    admins = User.query.filter_by(is_admin=True).all()

    result = [
        {"chat_id": admin.chat_id}
        for admin in admins
    ]

    return result, 200


@users_bp.route(
    "/users/<string:chat_id>/menu-version",
    methods=["PATCH"]
)
def update_menu_version(chat_id):

    user = User.query.filter_by(chat_id=chat_id).first()

    if not user:
        return {"error": "user not found"}, 404

    data = request.get_json()

    menu_version = data.get("menu_version")

    if menu_version is None:
        return {"error": "menu_version is required"}, 400

    user.menu_version = menu_version

    db.session.commit()

    return {"message": "menu_version updated"}, 200