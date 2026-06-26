from datetime import datetime, timedelta

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

    if service.recovery_days is None:

        return {
            "error": "service recovery days not set"
        }, 400

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

    repair_date = procedure_date + timedelta(
        days=service.recovery_days
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