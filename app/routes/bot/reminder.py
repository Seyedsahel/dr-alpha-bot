from datetime import datetime, timedelta, date

from flask import Blueprint, request

from app.extensions import db
from app.models.reminder import Reminder
from app.models.user import User
from app.models.service import Service


reminders_bp = Blueprint(
    "reminders",
    __name__
)


@reminders_bp.route(
    "/reminders",
    methods=["POST"]
)
def create_reminder():

    data = request.get_json()

    user_id = data.get("user_id")
    service_id = data.get("service_id")
    procedure_date = data.get("procedure_date")

    if not user_id or not service_id or not procedure_date:

        return {
            "error": "user_id, service_id and procedure_date are required"
        }, 400

    user = User.query.get(user_id)

    if not user:

        return {
            "error": "user not found"
        }, 404

    service = Service.query.get(service_id)

    if not service:

        return {
            "error": "service not found"
        }, 404


    exists = Reminder.query.filter_by(
        user_id=user_id,
        service_id=service_id,
        sent=False
    ).first()

    if exists:

        return {
            "error": "active reminder already exists"
        }, 400

    try:

        procedure_date = datetime.strptime(
            procedure_date,
            "%Y-%m-%d"
        ).date()

    except ValueError:

        return {
            "error": "invalid date format"
        }, 400
    
    recovery_days = service.recovery_days or 30
    repair_date = procedure_date + timedelta(
        days=recovery_days
    )

    reminder_date = repair_date - timedelta(
        days=3
    )

    reminder = Reminder(
        user_id=user_id,
        service_id=service_id,
        procedure_date=procedure_date,
        reminder_date=reminder_date
    )

    db.session.add(reminder)
    db.session.commit()

    return {
        "message": "reminder created",
        "reminder_id": reminder.id,
        "repair_date": repair_date.isoformat(),
        "reminder_date": reminder_date.isoformat()
    }, 201



@reminders_bp.route(
    "/reminders/<int:user_id>",
    methods=["GET"]
)
def get_user_reminders(user_id):

    user = User.query.get(user_id)

    if not user:
        return {
            "error": "user not found"
        }, 404

    reminders = Reminder.query.filter_by(
        user_id=user_id
    ).all()

    result = []

    for reminder in reminders:
        if reminder.sent:
            continue

        result.append({
            "id": reminder.id,
            "user_id": reminder.user_id,
            "service_id": reminder.service_id,
            "service_name": reminder.service.name if reminder.service else None,
            "procedure_date": reminder.procedure_date.isoformat(),
            "reminder_date": reminder.reminder_date.isoformat(),
            "sent": reminder.sent,
            "created_at": reminder.created_at.isoformat()
        })

    return result, 200


@reminders_bp.route(
    "/reminders/due",
    methods=["GET"]
)
def get_due_reminders():

    today = date.today()

    reminders = Reminder.query.filter(
        Reminder.sent == False,
        Reminder.reminder_date <= today
    ).all()

    result = []

    for reminder in reminders:

        result.append({
            "id": reminder.id,
            "chat_id": reminder.user.chat_id,
            "first_name": reminder.user.first_name,
            "service_name": reminder.service.name if reminder.service else None
        })

    return result, 200


@reminders_bp.route(
    "/reminders/<int:reminder_id>/mark-sent",
    methods=["POST"]
)
def mark_reminder_sent(reminder_id):

    reminder = Reminder.query.get(reminder_id)

    if not reminder:
        return {
            "error": "reminder not found"
        }, 404

    reminder.sent = True

    db.session.commit()

    return {
        "message": "reminder marked as sent"
    }, 200