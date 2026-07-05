import os

from flask import (
    Blueprint, render_template, request,
    redirect, url_for, session, flash, current_app
)

from app.extensions import db
from app.models.user import User
from app.models.available_slot import AvailableSlot
from app.models.appoinment import Appointment
from app.models.consultation import Consultation
from app.models.reminder import Reminder
from app.models.service import Service
from app.models.faq import FAQ
from app.models.aftercare import AfterCare
from app.models.festival import Festival
from app.utils.jalali import jalali_str_to_gregorian_datetime
from app.utils.file_handler import allowed_file, save_image, delete_image
from app.utils.auth import login_required

from app import limiter

admin_panel_bp = Blueprint(
    "admin_panel",
    __name__
)


# ---------- Auth ----------

@admin_panel_bp.route("/login", methods=["GET", "POST"])

@limiter.limit("5 per minute", methods=["POST"])

def login():

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        if (
            username == current_app.config["ADMIN_USERNAME"]
            and password == current_app.config["ADMIN_PASSWORD"]
        ):
            session["is_admin"] = True
            return redirect(url_for("admin_panel.dashboard"))

        flash("نام کاربری یا رمز عبور اشتباه است")

    return render_template("admin/login.html")


@admin_panel_bp.route("/logout")
def logout():

    session.pop("is_admin", None)

    return redirect(url_for("admin_panel.login"))


# ---------- Dashboard ----------

@admin_panel_bp.route("/")
@login_required
def dashboard():

    stats = {
        "users": User.query.count(),
        "pending_appointments": Appointment.query.filter_by(status="pending").count(),
        "pending_consultations": Consultation.query.filter_by(status="pending").count(),
        "active_reminders": Reminder.query.filter_by(sent=False).count(),
        "empty_slots": AvailableSlot.query.filter_by(is_booked=False).count()
    }

    return render_template("admin/dashboard.html", stats=stats)


# ---------- Users ----------

@admin_panel_bp.route("/users")
@login_required
def users():

    all_users = User.query.order_by(User.created_at.desc()).all()

    return render_template("admin/users.html", users=all_users)


# ---------- Slots ----------

@admin_panel_bp.route("/slots", methods=["GET", "POST"])
@login_required
def slots():

    if request.method == "POST":

        jalali_date = request.form.get("jalali_date")
        time_str = request.form.get("time")

        if not jalali_date or not time_str:
            flash("لطفاً تاریخ و ساعت را وارد کنید")
            return redirect(url_for("admin_panel.slots"))

        try:
            start_time = jalali_str_to_gregorian_datetime(jalali_date, time_str)
        except Exception:
            flash("تاریخ یا ساعت وارد شده معتبر نیست")
            return redirect(url_for("admin_panel.slots"))

        slot = AvailableSlot(start_time=start_time)
        db.session.add(slot)
        db.session.commit()

        flash("زمان خالی با موفقیت اضافه شد")

        return redirect(url_for("admin_panel.slots"))

    all_slots = AvailableSlot.query.order_by(AvailableSlot.start_time.desc()).all()

    return render_template("admin/slots.html", slots=all_slots)


@admin_panel_bp.route("/slots/<int:slot_id>/delete", methods=["POST"])
@login_required
def delete_slot(slot_id):

    slot = AvailableSlot.query.get(slot_id)

    if not slot:
        flash("زمان مورد نظر یافت نشد")
        return redirect(url_for("admin_panel.slots"))

    if slot.is_booked:
        flash("این زمان رزرو شده و قابل حذف نیست")
        return redirect(url_for("admin_panel.slots"))

    db.session.delete(slot)
    db.session.commit()

    flash("زمان حذف شد")

    return redirect(url_for("admin_panel.slots"))


# ---------- Appointments ----------

@admin_panel_bp.route("/appointments")
@login_required
def appointments():

    all_appointments = Appointment.query.order_by(Appointment.created_at.desc()).all()

    return render_template("admin/appointments.html", appointments=all_appointments)


@admin_panel_bp.route("/appointments/<int:appointment_id>/status", methods=["POST"])
@login_required
def update_appointment(appointment_id):

    appointment = Appointment.query.get(appointment_id)

    if not appointment:
        flash("نوبت یافت نشد")
        return redirect(url_for("admin_panel.appointments"))

    status = request.form.get("status")

    if status not in ("pending", "confirmed", "rejected"):
        flash("وضعیت نامعتبر است")
        return redirect(url_for("admin_panel.appointments"))

    appointment.status = status

    if status == "rejected":
        appointment.slot.is_booked = False
    else:
        appointment.slot.is_booked = True

    db.session.commit()

    flash("وضعیت نوبت بروزرسانی شد")

    return redirect(url_for("admin_panel.appointments"))


# ---------- Consultations ----------

@admin_panel_bp.route("/consultations")
@login_required
def consultations():

    all_consultations = Consultation.query.order_by(Consultation.created_at.desc()).all()

    return render_template("admin/consultations.html", consultations=all_consultations)


@admin_panel_bp.route("/consultations/<int:consultation_id>/status", methods=["POST"])
@login_required
def update_consultation(consultation_id):

    consultation = Consultation.query.get(consultation_id)

    if not consultation:
        flash("درخواست یافت نشد")
        return redirect(url_for("admin_panel.consultations"))

    status = request.form.get("status")

    if status not in ("pending", "called", "closed"):
        flash("وضعیت نامعتبر است")
        return redirect(url_for("admin_panel.consultations"))

    consultation.status = status

    db.session.commit()

    flash("وضعیت درخواست مشاوره بروزرسانی شد")

    return redirect(url_for("admin_panel.consultations"))


# ---------- Reminders (فقط نمایش) ----------

@admin_panel_bp.route("/reminders")
@login_required
def reminders():

    all_reminders = Reminder.query.order_by(Reminder.created_at.desc()).all()

    return render_template("admin/reminders.html", reminders=all_reminders)


# ---------- Services ----------

@admin_panel_bp.route("/services", methods=["GET", "POST"])
@login_required
def services():

    if request.method == "POST":

        name = request.form.get("name")
        price = request.form.get("price")
        description = request.form.get("description")
        recovery_days = request.form.get("recovery_days")

        if not name or not recovery_days:
            flash("نام خدمت و روزهای بهبودی الزامی است")
            return redirect(url_for("admin_panel.services"))

        if Service.query.filter_by(name=name).first():
            flash("این خدمت قبلاً ثبت شده است")
            return redirect(url_for("admin_panel.services"))

        service = Service(
            name=name,
            price=int(price) if price else None,
            description=description,
            recovery_days=int(recovery_days)
        )

        db.session.add(service)
        db.session.commit()

        flash("خدمت جدید ثبت شد")

        return redirect(url_for("admin_panel.services"))

    all_services = Service.query.order_by(Service.created_at.desc()).all()

    return render_template("admin/services.html", services=all_services)


@admin_panel_bp.route("/services/<int:service_id>/update", methods=["POST"])
@login_required
def update_service(service_id):

    service = Service.query.get(service_id)

    if not service:
        flash("خدمت یافت نشد")
        return redirect(url_for("admin_panel.services"))

    service.name = request.form.get("name", service.name)

    price = request.form.get("price")
    service.price = int(price) if price else None

    service.description = request.form.get("description")

    recovery_days = request.form.get("recovery_days")
    if recovery_days:
        service.recovery_days = int(recovery_days)

    service.is_active = request.form.get("is_active") == "on"

    db.session.commit()

    flash("خدمت بروزرسانی شد")

    return redirect(url_for("admin_panel.services"))


@admin_panel_bp.route("/services/<int:service_id>/delete", methods=["POST"])
@login_required
def delete_service(service_id):

    service = Service.query.get(service_id)

    if not service:
        flash("خدمت یافت نشد")
        return redirect(url_for("admin_panel.services"))

    service.is_active = False
    db.session.commit()

    flash("خدمت غیرفعال شد")

    return redirect(url_for("admin_panel.services"))


# ---------- FAQs ----------

@admin_panel_bp.route("/faqs", methods=["GET", "POST"])
@login_required
def faqs():

    if request.method == "POST":

        question = request.form.get("question")
        answer = request.form.get("answer")

        if not question or not answer:
            flash("سوال و جواب الزامی است")
            return redirect(url_for("admin_panel.faqs"))

        faq = FAQ(question=question, answer=answer)

        db.session.add(faq)
        db.session.commit()

        flash("سوال متداول اضافه شد")

        return redirect(url_for("admin_panel.faqs"))

    all_faqs = FAQ.query.order_by(FAQ.created_at.desc()).all()

    return render_template("admin/faqs.html", faqs=all_faqs)


@admin_panel_bp.route("/faqs/<int:faq_id>/update", methods=["POST"])
@login_required
def update_faq(faq_id):

    faq = FAQ.query.get(faq_id)

    if not faq:
        flash("سوال یافت نشد")
        return redirect(url_for("admin_panel.faqs"))

    faq.question = request.form.get("question", faq.question)
    faq.answer = request.form.get("answer", faq.answer)
    faq.is_active = request.form.get("is_active") == "on"

    db.session.commit()

    flash("سوال بروزرسانی شد")

    return redirect(url_for("admin_panel.faqs"))


@admin_panel_bp.route("/faqs/<int:faq_id>/delete", methods=["POST"])
@login_required
def delete_faq(faq_id):

    faq = FAQ.query.get(faq_id)

    if not faq:
        flash("سوال یافت نشد")
        return redirect(url_for("admin_panel.faqs"))

    faq.is_active = False
    db.session.commit()

    flash("سوال غیرفعال شد")

    return redirect(url_for("admin_panel.faqs"))


# ---------- Aftercares ----------

@admin_panel_bp.route("/aftercares", methods=["GET", "POST"])
@login_required
def aftercares():

    if request.method == "POST":

        service_id = request.form.get("service_id")
        content = request.form.get("content")

        if not service_id or not content:
            flash("انتخاب خدمت و متن الزامی است")
            return redirect(url_for("admin_panel.aftercares"))

        if AfterCare.query.filter_by(service_id=service_id).first():
            flash("برای این خدمت قبلاً مراقبت ثبت شده است")
            return redirect(url_for("admin_panel.aftercares"))

        aftercare = AfterCare(service_id=int(service_id), content=content)

        db.session.add(aftercare)
        db.session.commit()

        flash("مراقبت بعد از خدمت اضافه شد")

        return redirect(url_for("admin_panel.aftercares"))

    all_aftercares = AfterCare.query.all()
    all_services = Service.query.filter_by(is_active=True).all()

    return render_template(
        "admin/aftercares.html",
        aftercares=all_aftercares,
        services=all_services
    )


@admin_panel_bp.route("/aftercares/<int:aftercare_id>/update", methods=["POST"])
@login_required
def update_aftercare(aftercare_id):

    aftercare = AfterCare.query.get(aftercare_id)

    if not aftercare:
        flash("مورد یافت نشد")
        return redirect(url_for("admin_panel.aftercares"))

    aftercare.content = request.form.get("content", aftercare.content)
    aftercare.is_active = request.form.get("is_active") == "on"

    db.session.commit()

    flash("بروزرسانی شد")

    return redirect(url_for("admin_panel.aftercares"))


@admin_panel_bp.route("/aftercares/<int:aftercare_id>/delete", methods=["POST"])
@login_required
def delete_aftercare(aftercare_id):

    aftercare = AfterCare.query.get(aftercare_id)

    if not aftercare:
        flash("مورد یافت نشد")
        return redirect(url_for("admin_panel.aftercares"))

    aftercare.is_active = False
    db.session.commit()

    flash("غیرفعال شد")

    return redirect(url_for("admin_panel.aftercares"))


# ---------- Festivals ----------

@admin_panel_bp.route("/festivals", methods=["GET", "POST"])
@login_required
def festivals():

    if request.method == "POST":

        title = request.form.get("title")
        description = request.form.get("description")
        image = request.files.get("image")

        if not title or not description:
            flash("عنوان و توضیحات الزامی است")
            return redirect(url_for("admin_panel.festivals"))

        filename = None

        if image and image.filename:

            if not allowed_file(image.filename):
                flash("فرمت تصویر نامعتبر است")
                return redirect(url_for("admin_panel.festivals"))

            filename = save_image(
                image,
                os.path.join(current_app.config["UPLOAD_FOLDER"], "festivals")
            )

        festival = Festival(title=title, description=description, image_path=filename)

        db.session.add(festival)
        db.session.commit()

        flash("جشنواره اضافه شد")

        return redirect(url_for("admin_panel.festivals"))

    all_festivals = Festival.query.order_by(Festival.created_at.desc()).all()

    return render_template("admin/festivals.html", festivals=all_festivals)


@admin_panel_bp.route("/festivals/<int:festival_id>/update", methods=["POST"])
@login_required
def update_festival(festival_id):

    festival = Festival.query.get(festival_id)

    if not festival:
        flash("جشنواره یافت نشد")
        return redirect(url_for("admin_panel.festivals"))

    title = request.form.get("title")
    description = request.form.get("description")

    if title:
        festival.title = title

    if description:
        festival.description = description

    image = request.files.get("image")

    if image and image.filename:

        if not allowed_file(image.filename):
            flash("فرمت تصویر نامعتبر است")
            return redirect(url_for("admin_panel.festivals"))

        delete_image(
            festival.image_path,
            os.path.join(current_app.config["UPLOAD_FOLDER"], "festivals")
        )

        festival.image_path = save_image(
            image,
            os.path.join(current_app.config["UPLOAD_FOLDER"], "festivals")
        )

    festival.is_active = request.form.get("is_active") == "on"

    db.session.commit()

    flash("جشنواره بروزرسانی شد")

    return redirect(url_for("admin_panel.festivals"))


@admin_panel_bp.route("/festivals/<int:festival_id>/delete", methods=["POST"])
@login_required
def delete_festival(festival_id):

    festival = Festival.query.get(festival_id)

    if not festival:
        flash("جشنواره یافت نشد")
        return redirect(url_for("admin_panel.festivals"))

    if festival.image_path:

        delete_image(
            festival.image_path,
            os.path.join(current_app.config["UPLOAD_FOLDER"], "festivals")
        )

        festival.image_path = None

    festival.is_active = False

    db.session.commit()

    flash("جشنواره غیرفعال شد")

    return redirect(url_for("admin_panel.festivals"))