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
            "minimum_price": service.minimum_price,
            "maximum_price": service.maximum_price,
            "price": service.minimum_price,
            "description": service.description
        })

    return result, 200