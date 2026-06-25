from flask import Blueprint

from app.models.appoinment import Appointment

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

        result.append({
            "id": appointment.id,
            "user_id": appointment.user_id,
            "service": appointment.service,
            "status": appointment.status,
            "slot_time": appointment.slot.start_time.strftime(
                "%Y-%m-%d %H:%M"
            )
        })

    return result, 200