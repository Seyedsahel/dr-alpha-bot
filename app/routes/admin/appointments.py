from flask import Blueprint, request

from app.models.appoinment import Appointment
from app.extensions import db

admin_appointments_bp = Blueprint(
    "admin_appointments",
    __name__
)

@admin_appointments_bp.route(
    "/appointments",
    methods=["GET"]
)
def get_appointments():

    appointments = Appointment.query.all()

    result = []

    for appointment in appointments:

        full_name = ""
        if appointment.user:
            first_name = appointment.user.first_name or ""
            last_name = appointment.user.last_name or ""
            full_name = f"{first_name} {last_name}".strip()

        result.append({
            "id": appointment.id,
            "name": full_name,
            "phone": appointment.user.phone if appointment.user else None,
            "service_name": appointment.service.name,
            "service_id": appointment.service_id,
            "status": appointment.status,
            "slot_time": appointment.slot.start_time.strftime(
                "%Y-%m-%d %H:%M"
            )
        })

    return result, 200


@admin_appointments_bp.route(
    "/appointments/<int:appointment_id>",
    methods=["PATCH"]
)
def update_appointment_status(appointment_id):

    appointment = Appointment.query.get(
        appointment_id
    )

    if not appointment:
        return {
            "error": "نوبت پیدا نشد"
        }, 404

    data = request.get_json()

    status = data.get("status")

    allowed_statuses = [
        "pending",
        "confirmed",
        "rejected"
    ]

    if status not in allowed_statuses:
        return {
            "error": "invalid status"
        }, 400

    appointment.status = status
    
    if status == "rejected":
        appointment.slot.is_booked = False
    else:
        appointment.slot.is_booked = True

    db.session.commit()

    return {
        "message": "appointment updated",
        "status": appointment.status
    }, 200