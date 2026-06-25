from flask import Blueprint,request
from app.extensions import db
from app.models.consultation import Consultation

admin_consultations_bp = Blueprint(
    "admin_consultations",
    __name__
)

from app.models.consultation import Consultation


@admin_consultations_bp.route(
    "/consultations",
    methods=["GET"]
)
def get_consultations():

    consultations = Consultation.query.all()

    result = []

    for consultation in consultations:

        result.append({
            "id": consultation.id,
            "name": f"{consultation.user.first_name} {consultation.user.last_name}",
            "phone": consultation.user.phone,
            "service": consultation.service,
            "note": consultation.note,
            "status": consultation.status
        })

    return result, 200


@admin_consultations_bp.route(
    "/consultations/<int:consultation_id>",
    methods=["PATCH"]
)
def update_consultation_status(
    consultation_id
):

    consultation = Consultation.query.get(
        consultation_id
    )

    if not consultation:
        return {
            "error": "consultation not found"
        }, 404

    data = request.get_json()

    status = data.get("status")

    allowed_statuses = [
        "pending",
        "called",
        "closed"
    ]

    if status not in allowed_statuses:
        return {
            "error": "invalid status"
        }, 400

    consultation.status = status

    db.session.commit()

    return {
        "message": "consultation updated",
        "status": consultation.status
    }