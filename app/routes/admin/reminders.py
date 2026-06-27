from flask import Blueprint

from app.models.reminder import Reminder

admin_reminders_bp = Blueprint(
    "admin_reminders",
    __name__
)


@admin_reminders_bp.route(
    "/reminders",
    methods=["GET"]
)
def get_reminders():

    reminders = Reminder.query.all()

    result = []

    for reminder in reminders:

        result.append({
            "id": reminder.id,
            "user_id": reminder.user_id,
            "user_name": f"{reminder.user.first_name} {reminder.user.last_name}",
            "service_id": reminder.service_id,
            "service_name": reminder.service.name,
            "procedure_date": reminder.procedure_date.isoformat(),
            "reminder_date": reminder.reminder_date.isoformat(),
            "sent": reminder.sent,
            "created_at": reminder.created_at.isoformat()
        })

    return result, 200

@admin_reminders_bp.route(
    "/reminders/<int:reminder_id>",
    methods=["GET"]
)
def get_reminder(reminder_id):

    reminder = Reminder.query.get(reminder_id)

    if not reminder:

        return {
            "error": "reminder not found"
        }, 404

    return {
        "id": reminder.id,
        "user_id": reminder.user_id,
        "user_name": f"{reminder.user.first_name} {reminder.user.last_name}",
        "service_id": reminder.service_id,
        "service_name": reminder.service.name,
        "procedure_date": reminder.procedure_date.isoformat(),
        "reminder_date": reminder.reminder_date.isoformat(),
        "sent": reminder.sent,
        "created_at": reminder.created_at.isoformat()
    }, 200