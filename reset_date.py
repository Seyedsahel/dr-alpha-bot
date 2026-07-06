# reset_data.py — یک‌بار مصرف، بعدش پاکش کن

from app import create_app
from app.extensions import db
from app.models import (
    User, AvailableSlot, Appointment,
    Consultation, Reminder, Service,
    FAQ, AfterCare, Festival
)

app = create_app()

with app.app_context():

    for model in [
        Appointment, Consultation, Reminder,
        AvailableSlot, AfterCare, Service,
        FAQ, Festival, User
    ]:
        db.session.query(model).delete()

    db.session.commit()

    print("همه‌ی دیتا پاک شد.")