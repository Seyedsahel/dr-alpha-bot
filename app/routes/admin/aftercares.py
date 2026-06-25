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
            "id":aftercare.id,
            "service_name":aftercare.service_name,
            "content":aftercare.content
        })

    return result,200

@admin_aftercares_bp.route(
    "/aftercares",
    methods=["POST"]
)
def create_aftercare():

    data = request.get_json()

    service_name = data.get("service_name")
    content = data.get("content")

    if not service_name or not content:

        return {
            "error":"service_name and content are required"
        },400

    aftercare = AfterCare(
        service_name=service_name,
        content=content
    )

    db.session.add(aftercare)
    db.session.commit()

    return {
        "message":"aftercare created",
        "aftercare_id":aftercare.id
    },201

@admin_aftercares_bp.route(
    "/aftercares/<int:aftercare_id>",
    methods=["PATCH"]
)
def update_aftercare(aftercare_id):

    aftercare = AfterCare.query.get(aftercare_id)

    if not aftercare:

        return {
            "error":"aftercare not found"
        },404

    data = request.get_json()

    if "service_name" in data:
        aftercare.service_name = data["service_name"]

    if "content" in data:
        aftercare.content = data["content"]

    db.session.commit()

    return {
        "message":"aftercare updated"
    },200

@admin_aftercares_bp.route(
    "/aftercares/<int:aftercare_id>",
    methods=["DELETE"]
)
def delete_aftercare(aftercare_id):

    aftercare = AfterCare.query.get(aftercare_id)

    if not aftercare:

        return {
            "error":"aftercare not found"
        },404

    db.session.delete(aftercare)
    db.session.commit()

    return {
        "message":"aftercare deleted"
    },200