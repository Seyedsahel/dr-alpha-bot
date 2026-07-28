from flask import Blueprint, request

from app.extensions import db
from app.models.service_category import ServiceCategory

admin_service_categories_bp = Blueprint(
    "admin_service_categories",
    __name__
)


@admin_service_categories_bp.route(
    "/service-categories",
    methods=["GET"]
)
def get_service_categories():

    categories = ServiceCategory.query.all()

    result = []

    for category in categories:

        result.append({
            "id": category.id,
            "name": category.name,
            "service_count": len(category.services)
        })

    return result, 200


@admin_service_categories_bp.route(
    "/service-categories",
    methods=["POST"]
)
def create_service_category():

    data = request.get_json()

    name = data.get("name")

    if not name:
        return {"error": "name is required"}, 400

    if ServiceCategory.query.filter_by(name=name).first():
        return {"error": "category already exists"}, 409

    category = ServiceCategory(name=name)

    db.session.add(category)
    db.session.commit()

    return {
        "message": "category created",
        "category_id": category.id
    }, 201


@admin_service_categories_bp.route(
    "/service-categories/<int:category_id>",
    methods=["DELETE"]
)
def delete_service_category(category_id):

    category = ServiceCategory.query.get(category_id)

    if not category:
        return {"error": "category not found"}, 404

    for service in category.services:
        service.category_id = None

    db.session.delete(category)
    db.session.commit()

    return {"message": "category deleted"}, 200