from flask import Blueprint
from app.models.available_slot import AvailableSlot

bot_slots_bp = Blueprint(
    "bot_slots",
    __name__
)


@bot_slots_bp.route("/slots", methods=["GET"])
def get_available_slots():

    slots = AvailableSlot.query.filter_by(
        is_booked=False
    ).all()

    result = []

    for slot in slots:

        result.append({
            "id": slot.id,
            "start_time": slot.start_time.strftime(
                "%Y-%m-%d %H:%M"
            )
        })

    return result, 200