from flask import Blueprint, current_app

from app.models.clinic_info import ClinicInfo
from app.models.doctor import Doctor

clinic_info_bp = Blueprint(
    "clinic_info",
    __name__
)


@clinic_info_bp.route(
    "/clinic-info",
    methods=["GET"]
)
def get_clinic_info():

    info = ClinicInfo.query.first()

    doctors = Doctor.query.filter_by(is_active=True).all()

    doctors_result = []

    for doctor in doctors:

        photo_url = None

        if doctor.photo_path:
            photo_url = (
                f"{current_app.config['PUBLIC_BASE_URL']}"
                f"/uploads/doctors/{doctor.photo_path}"
            )

        doctors_result.append({
            "id": doctor.id,
            "name": doctor.name,
            "medical_license_number": doctor.medical_license_number,
            "photo_url": photo_url
        })

    return {
        "address": info.address if info else None,
        "phone": info.phone if info else None,
        "website": info.website if info else None,
        "instagram": info.instagram if info else None,
        "bale_channel": info.bale_channel if info else None,
        "doctors": doctors_result
    }, 200