from flask import Blueprint, request

from app.extensions import db
from app.models.clinic_info import ClinicInfo

admin_clinic_info_bp = Blueprint(
    "admin_clinic_info",
    __name__
)


def get_or_create_clinic_info():

    info = ClinicInfo.query.first()

    if not info:
        info = ClinicInfo()
        db.session.add(info)
        db.session.commit()

    return info


@admin_clinic_info_bp.route(
    "/clinic-info",
    methods=["GET"]
)
def get_clinic_info():

    info = get_or_create_clinic_info()

    return {
        "address": info.address,
        "phone": info.phone,
        "website": info.website,
        "instagram": info.instagram,
        "bale_channel": info.bale_channel
    }, 200


@admin_clinic_info_bp.route(
    "/clinic-info",
    methods=["PATCH"]
)
def update_clinic_info():

    info = get_or_create_clinic_info()

    data = request.get_json()

    for field in ("address", "phone", "website", "instagram", "bale_channel"):
        if field in data:
            setattr(info, field, data[field])

    db.session.commit()

    return {"message": "clinic info updated"}, 200