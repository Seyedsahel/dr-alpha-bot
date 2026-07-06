from flask import Blueprint, request

from sqlalchemy.exc import IntegrityError

from app.extensions import db
from app.models.appoinment import Appointment
from app.models.available_slot import AvailableSlot

appointments_bp = Blueprint(
    "appointments",
    __name__
)


@appointments_bp.route(
    "/appointments",
    methods=["POST"]
)
def create_appointment():

    data = request.get_json()

    user_id = data.get("user_id")
    slot_id = data.get("slot_id")
    service_id = data.get("service_id")
    description = data.get("description")

    if not user_id or not slot_id or not service_id:
        return {
            "error": "اطلاعات ناقص است"
        }, 400

    slot = AvailableSlot.query.get(slot_id)

    if not slot:
        return {
            "error": "زمان خالی وجود ندارد"
        }, 404

    if slot.is_booked:
        return {
            "error": "این نوبت پر شده است"
        }, 400

    appointment = Appointment(
        user_id=user_id,
        slot_id=slot_id,
        service_id=service_id,
        description=description
    )

    slot.is_booked = True

    db.session.add(appointment)

    try:
        db.session.commit()

    except IntegrityError:

        db.session.rollback()

        return {
            "error": "این نوبت لحظاتی پیش توسط شخص دیگری رزرو شد"
        }, 409

    return {
        "message": "نوبت ثبت شد",
        "appointment_id": appointment.id
    }, 201


@appointments_bp.route(
    "/appointments/<int:user_id>",
    methods=["GET"]
)
def get_user_appointments(user_id):

    appointments = Appointment.query.filter_by(
        user_id=user_id
    ).order_by(
        Appointment.created_at.desc()
    ).all()

    result = []

    for appointment in appointments:

        result.append({
            "id": appointment.id,
            "service_name": appointment.service.name if appointment.service else None,
            "slot_time": appointment.slot.start_time.isoformat() if appointment.slot else None,
            "status": appointment.status,
            "created_at": appointment.created_at.isoformat()
        })

    return result, 200