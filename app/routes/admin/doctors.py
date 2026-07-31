import os

from flask import Blueprint, request, current_app

from app.extensions import db
from app.models.doctor import Doctor
from app.utils.file_handler import (
    allowed_file,
    save_image,
    delete_image
)

admin_doctors_bp = Blueprint(
    "admin_doctors",
    __name__
)


@admin_doctors_bp.route(
    "/doctors",
    methods=["GET"]
)
def get_doctors():

    doctors = Doctor.query.all()

    result = []

    for doctor in doctors:

        result.append({
            "id": doctor.id,
            "name": doctor.name,
            "medical_license_number": doctor.medical_license_number,
            "photo_path": doctor.photo_path,
            "is_active": doctor.is_active
        })

    return result, 200


@admin_doctors_bp.route(
    "/doctors",
    methods=["POST"]
)
def create_doctor():

    name = request.form.get("name")
    medical_license_number = request.form.get("medical_license_number")
    image = request.files.get("photo")

    if not name:
        return {"error": "name is required"}, 400

    filename = None

    if image and image.filename:

        if not allowed_file(image.filename):
            return {"error": "invalid image format"}, 400

        filename = save_image(
            image,
            os.path.join(current_app.config["UPLOAD_FOLDER"], "doctors")
        )

    doctor = Doctor(
        name=name,
        medical_license_number=medical_license_number,
        photo_path=filename
    )

    db.session.add(doctor)
    db.session.commit()

    return {
        "message": "doctor created",
        "doctor_id": doctor.id
    }, 201


@admin_doctors_bp.route(
    "/doctors/<int:doctor_id>",
    methods=["PATCH"]
)
def update_doctor(doctor_id):

    doctor = Doctor.query.get(doctor_id)

    if not doctor:
        return {"error": "doctor not found"}, 404

    name = request.form.get("name")
    medical_license_number = request.form.get("medical_license_number")
    is_active = request.form.get("is_active")
    image = request.files.get("photo")

    if name:
        doctor.name = name

    if medical_license_number is not None:
        doctor.medical_license_number = medical_license_number

    doctors_folder = os.path.join(current_app.config["UPLOAD_FOLDER"], "doctors")

    if image and image.filename:

        if not allowed_file(image.filename):
            return {"error": "invalid image format"}, 400

        delete_image(doctors_folder, doctor.photo_path)

        doctor.photo_path = save_image(image, doctors_folder)

    if is_active is not None:
        doctor.is_active = is_active.lower() == "true"

    db.session.commit()

    return {"message": "doctor updated"}, 200


@admin_doctors_bp.route(
    "/doctors/<int:doctor_id>",
    methods=["DELETE"]
)
def delete_doctor(doctor_id):

    doctor = Doctor.query.get(doctor_id)

    if not doctor:
        return {"error": "doctor not found"}, 404

    doctor.is_active = False

    db.session.commit()

    return {"message": "doctor deactivated"}, 200

@admin_doctors_bp.route(
    "/doctors/<int:doctor_id>/permanent",
    methods=["DELETE"]
)
def delete_doctor_permanently(doctor_id):

    doctor = Doctor.query.get(doctor_id)

    if not doctor:
        return {"error": "doctor not found"}, 404

    if doctor.photo_path:

        doctors_folder = os.path.join(current_app.config["UPLOAD_FOLDER"], "doctors")

        delete_image(doctors_folder, doctor.photo_path)

    db.session.delete(doctor)
    db.session.commit()

    return {"message": "doctor permanently deleted"}, 200