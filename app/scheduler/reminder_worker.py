import threading
import time

from app.scheduler.reminder_service import process_reminders

def worker(app):

    with app.app_context():

        while True:
            try:
                process_reminders()

            except Exception as error:
                print(f"[Reminder Worker Error] {error}")

            time.sleep(60)

def start_worker(app):

    thread = threading.Thread(
        target=worker,
        args=(app,),
        daemon=True
    )

    thread.start()