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

        full_name = ""
        if appointment.user:
            first_name = appointment.user.first_name or ""
            last_name = appointment.user.last_name or ""
            full_name = f"{first_name} {last_name}".strip()

        result.append({
            "id": appointment.id,
            "name": full_name,
            "phone": appointment.user.phone if appointment.user else None,
            "service": appointment.service,
            "status": appointment.status,
            "slot_time": appointment.slot.start_time.strftime(
                "%Y-%m-%d %H:%M"
            )
        })

    return result, 200