from flask import Blueprint

from app.models.user import User

admin_users_bp = Blueprint(
    "admin_users",
    __name__
)


@admin_users_bp.route(
    "/users",
    methods=["GET"]
)
def get_users():

    users = User.query.order_by(User.created_at.desc()).all()

    result = []

    for user in users:

        result.append({
            "id": user.id,
            "chat_id": user.chat_id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "phone": user.phone,
            "created_at": user.created_at.isoformat()
        })

    return result, 200