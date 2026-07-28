from flask import Blueprint

from app.models.service import Service
from app.models.service_category import ServiceCategory

service_categories_bp = Blueprint(
    "service_categories",
    __name__
)


@service_categories_bp.route(
    "/service-categories",
    methods=["GET"]
)
def get_service_categories():

    categories = ServiceCategory.query.all()

    result = []

    for category in categories:

        has_active_service = any(
            service.is_active for service in category.services
        )

        if has_active_service:
            result.append({
                "id": category.id,
                "name": category.name
            })

    has_uncategorized = Service.query.filter_by(
        category_id=None,
        is_active=True
    ).first() is not None

    if has_uncategorized:
        result.append({
            "id": None,
            "name": "سایر خدمات"
        })

    return result, 200