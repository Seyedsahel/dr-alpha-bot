from flask import Blueprint, request

from app.models.service import Service
from app.utils.validators import safe_int

services_bp = Blueprint(
    "services",
    __name__
)


@services_bp.route(
    "/services",
    methods=["GET"]
)
def get_services():

    category_id = request.args.get("category_id")

    query = Service.query.filter_by(is_active=True)

    if category_id is not None:

        if category_id == "none":
            query = query.filter_by(category_id=None)
        else:
            query = query.filter_by(category_id=safe_int(category_id))

    services = query.all()

    result = []

    for service in services:

        result.append({
            "id": service.id,
            "name": service.name,
            "minimum_price": service.minimum_price,
            "maximum_price": service.maximum_price,
            "price": service.minimum_price,
            "description": service.description,
            "category_id": service.category_id
        })

    return result, 200