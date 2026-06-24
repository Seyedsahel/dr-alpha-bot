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