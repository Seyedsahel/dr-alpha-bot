from flask import Blueprint, request

from app.models.service import Service
from app.extensions import db

admin_services_bp = Blueprint(
    "admin_services",
    __name__
)

@admin_services_bp.route(
    "/services",
    methods=["GET"]
)
def get_services():

    services = Service.query.all()

    result = []

    for service in services:

        result.append({
            "id": service.id,
            "name": service.name,
            "price": service.price,
            "description": service.description,
            "is_active": service.is_active
        })

    return result, 200