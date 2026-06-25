from flask import Blueprint, request
from app.extensions import db
from app.models.festival import Festival

admin_festivals_bp = Blueprint("admin_festivals", __name__)


@admin_festivals_bp.route("/festivals", methods=["GET"])
def get_festivals():

    festivals = Festival.query.all()

    result = []

    for festival in festivals:
        result.append({
            "id": festival.id,
            "title": festival.title,
            "description": festival.description,
            "is_active": festival.is_active,
            "created_at": festival.created_at
        })

    return result, 200

@admin_festivals_bp.route("/festivals", methods=["POST"])
def create_festival():

    data = request.get_json()

    title = data.get("title")
    description = data.get("description")

    if not title or not description:
        return {"error": "title and description are required"}, 400

    festival = Festival(
        title=title,
        description=description
    )

    db.session.add(festival)
    db.session.commit()

    return {
        "message": "festival created",
        "festival_id": festival.id
    }, 201

@admin_festivals_bp.route("/festivals/<int:festival_id>", methods=["PATCH"])
def update_festival(festival_id):

    festival = Festival.query.get(festival_id)

    if not festival:
        return {"error": "festival not found"}, 404

    data = request.get_json()

    if "title" in data:
        festival.title = data["title"]

    if "description" in data:
        festival.description = data["description"]

    if "is_active" in data:
        festival.is_active = data["is_active"]

    db.session.commit()

    return {"message": "festival updated"}, 200

@admin_festivals_bp.route("/festivals/<int:festival_id>", methods=["DELETE"])
def delete_festival(festival_id):

    festival = Festival.query.get(festival_id)

    if not festival:
        return {"error": "festival not found"}, 404

    festival.is_active = False

    db.session.commit()

    return {"message": "festival deactivated"}, 200