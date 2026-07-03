from flask import Blueprint, request
from app.models.consultation import Consultation
from app.extensions import db

consultations_bp = Blueprint(
    "consultations",
    __name__
)


@consultations_bp.route(
    "/consultations",
    methods=["POST"]
)
def create_consultation():

    data = request.get_json()

    user_id = data.get("user_id")

    if not user_id:
        return {
            "error": "user_id is required"
        }, 400

    consultation = Consultation(
        user_id=user_id,
        service=data.get("service"),
        note=data.get("note")
    )

    db.session.add(consultation)
    db.session.commit()

    return {
        "message": "consultation created",
        "consultation_id": consultation.id
    }, 201

@consultations_bp.route(
    "/consultations/<int:user_id>",
    methods=["GET"]
)
def get_user_consultations(user_id):

    consultations = Consultation.query.filter_by(
        user_id=user_id
    ).order_by(
        Consultation.created_at.desc()
    ).all()

    result = []

    for consultation in consultations:

        result.append({
            "id": consultation.id,
            "service": consultation.service,
            "note": consultation.note,
            "status": consultation.status,
            "created_at": consultation.created_at.isoformat()
        })

    return result, 200