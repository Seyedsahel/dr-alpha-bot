from flask import Blueprint

from app.models.service import Service

services_bp = Blueprint(
    "services",
    __name__
)

@services_bp.route(
    "/services",
    methods=["GET"]
)
def get_services():

    services = Service.query.filter_by(
        is_active=True
    ).all()

    result = []

    for service in services:

        result.append({
            "id": service.id,
            "name": service.name,
            "price": service.price,
            "description": service.description
        })

    return result, 200