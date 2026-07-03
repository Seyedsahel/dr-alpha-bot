from flask import Blueprint
import jdatetime

from app.models.available_slot import AvailableSlot

bot_slots_bp = Blueprint(
    "bot_slots",
    __name__
)


def to_jalali_datetime_str(value):

    jalali_date = jdatetime.date.fromgregorian(
        date=value.date()
    )

    return f"{jalali_date.strftime('%Y/%m/%d')} - {value.strftime('%H:%M')}"


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
            ),
            "start_time_jalali": to_jalali_datetime_str(
                slot.start_time
            )
        })

    return result, 200