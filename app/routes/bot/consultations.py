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
