from datetime import date

from app.extensions import db
from app.models.reminder import Reminder

def process_reminders():

    today = date.today()

    reminders = Reminder.query.filter(
        Reminder.sent == False,
        Reminder.reminder_date <= today
    ).all()

    for reminder in reminders:
        # Process each reminder (e.g., send bale message)
        # For demonstration purposes, we'll just print the reminder details
        # Optionally, you can mark the reminder as processed or delete it
        print("=" * 30)
        print("Reminder Triggered")
        print(f"Reminder ID: {reminder.id}")
        print(f"User: {reminder.user.first_name}")
        print(f"Chat ID: {reminder.user.chat_id}")
        print(f"Service: {reminder.service.name}")
        print(f"Reminder Date: {reminder.reminder_date}")
        print("=" * 30)
        # db.session.delete(reminder)  # Uncomment to delete after processing
        reminder.sent = True
        
    db.session.commit()  # Commit any changes made to the database