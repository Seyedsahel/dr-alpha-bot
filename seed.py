from datetime import datetime

from app import create_app
from app.extensions import db

from app.models.user import User
from app.models.available_slot import AvailableSlot
from app.models.service import Service
from app.models.faq import FAQ
from app.models.aftercare import AfterCare


app = create_app()


def seed_users():
    users = [
        {"chat_id": "1001", "first_name": "علی", "last_name": "احمدی", "phone": "09120000001"},
        {"chat_id": "1002", "first_name": "مریم", "last_name": "رضایی", "phone": "09120000002"},
        {"chat_id": "1003", "first_name": "حسین", "last_name": "محمدی", "phone": "09120000003"},
    ]

    for user_data in users:
        exists = User.query.filter_by(chat_id=user_data["chat_id"]).first()

        if not exists:
            db.session.add(User(**user_data))


def seed_slots():
    slots = [
        "2026-07-01 09:00",
        "2026-07-01 10:00",
        "2026-07-01 11:00",
        "2026-07-01 12:00",
        "2026-07-01 13:00",
    ]

    for slot in slots:
        slot_time = datetime.strptime(slot, "%Y-%m-%d %H:%M")

        exists = AvailableSlot.query.filter_by(start_time=slot_time).first()

        if not exists:
            db.session.add(AvailableSlot(start_time=slot_time))


def seed_services():
    services = [
        ("بوتاکس کامل صورت", 2200000),
        ("ژل لب", 6000000),
        ("مزو مو", 5000000),
        ("مزو جوانساز", 5000000),
    ]

    for name, price in services:
        exists = Service.query.filter_by(name=name).first()

        if not exists:
            db.session.add(Service(name=name, price=price))


def seed_faqs():
    faqs = [
        ("برند بوتاکس مورد استفاده چیست؟", "Masport"),
        ("ماندگاری بوتاکس چقدر است؟", "معمولاً بین ۳ تا ۶ ماه"),
        ("ماندگاری ژل چقدر است؟", "بسته به نوع ژل بین ۶ تا ۱۸ ماه"),
    ]

    for question, answer in faqs:
        exists = FAQ.query.filter_by(question=question).first()

        if not exists:
            db.session.add(FAQ(question=question, answer=answer))


def seed_aftercares():
    items = [
        ("بوتاکس کامل صورت", "تا ۴ ساعت دراز نکشید."),
        ("ژل لب", "تا ۲۴ ساعت از ماساژ ناحیه خودداری کنید."),
    ]

    for service_name, content in items:

        service = Service.query.filter_by(name=service_name).first()

        if not service:
            continue

        exists = AfterCare.query.filter_by(service_id=service.id).first()

        if not exists:
            db.session.add(
                AfterCare(
                    service_id=service.id,
                    content=content,
                )
            )


with app.app_context():
    seed_users()
    seed_slots()
    seed_services()
    seed_faqs()
    seed_aftercares()

    db.session.commit()

    print("Seed completed.")