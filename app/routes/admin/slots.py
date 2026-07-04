from flask import Blueprint, request
from datetime import datetime

from app.extensions import db
from app.models.available_slot import AvailableSlot

admin_slots_bp = Blueprint(
    "admin_slots",
    __name__
)

@admin_slots_bp.route("/slots", methods=["POST"])
def create_slot():
    data = request.get_json()
    start_time = data.get("start_time")
    
    if not start_time:
        return{
            "error":"لطفا تاریخ ازاد را وارد کنید"
        }, 400
    slot = AvailableSlot(
        start_time = datetime.strptime(
            start_time,
            "%Y-%m-%d %H:%M"
        )
    )
    db.session.add(slot)
    db.session.commit()


    return {
        "message": "slot created",
        "slot_id": slot.id
    }, 201

@admin_slots_bp.route("/slots", methods=["GET"])
def get_slots():

    slots = AvailableSlot.query.order_by(AvailableSlot.start_time.desc()).all()

    result = []

    for slot in slots:

        result.append({
            "id": slot.id,
            "start_time": slot.start_time.strftime("%Y-%m-%d %H:%M"),
            "is_booked": slot.is_booked
        })

    return result, 200


@admin_slots_bp.route("/slots/<int:slot_id>", methods=["DELETE"])
def delete_slot(slot_id):

    slot = AvailableSlot.query.get(slot_id)

    if not slot:
        return {"error": "slot not found"}, 404

    if slot.is_booked:
        return {"error": "cannot delete a booked slot"}, 400

    db.session.delete(slot)
    db.session.commit()

    return {"message": "slot deleted"}, 200