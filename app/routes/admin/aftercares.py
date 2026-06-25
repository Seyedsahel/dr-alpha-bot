from flask import Blueprint, request

from app.extensions import db
from app.models.aftercare import AfterCare

admin_aftercares_bp = Blueprint(
    "admin_aftercares",
    __name__
)

@admin_aftercares_bp.route(
    "/aftercares",
    methods=["GET"]
)
def get_aftercares():

    aftercares = AfterCare.query.all()

    result = []

    for aftercare in aftercares:
        result.append({
            "id": aftercare.id,
            "service_id": aftercare.service_id,
            "service_name": aftercare.service.name if aftercare.service else None,
            "content": aftercare.content,
            "is_active": aftercare.is_active
        })


    return result,200

@admin_aftercares_bp.route("/aftercares",
    methods=["POST"])
def create_aftercare():

    data = request.get_json()

    service_id = data.get("service_id")
    content = data.get("content")

    if not service_id or not content:
        return {"error": "service_id and content are required"}, 400

    exists = AfterCare.query.filter_by(service_id=service_id).first()
    if exists:
        return {"error": "aftercare already exists for this service"}, 400

    aftercare = AfterCare(
        service_id=service_id,
        content=content
    )

    db.session.add(aftercare)
    db.session.commit()

    return {
        "message": "aftercare created",
        "aftercare_id": aftercare.id
    }, 201

@admin_aftercares_bp.route("/aftercares/<int:aftercare_id>", methods=["PATCH"])
def update_aftercare(aftercare_id):

    aftercare = AfterCare.query.get(aftercare_id)

    if not aftercare:
        return {"error": "aftercare not found"}, 404

    data = request.get_json()

    if "service_id" in data:
        aftercare.service_id = data["service_id"]

    if "content" in data:
        aftercare.content = data["content"]

    if "is_active" in data:
        aftercare.is_active = data["is_active"]

    db.session.commit()

    return {"message": "aftercare updated"}, 200

@admin_aftercares_bp.route("/aftercares/<int:aftercare_id>", methods=["DELETE"])
def delete_aftercare(aftercare_id):

    aftercare = AfterCare.query.get(aftercare_id)

    if not aftercare:
        return {"error": "aftercare not found"}, 404

    aftercare.is_active = False

    db.session.commit()

    return {"message": "aftercare deactivated"}, 200