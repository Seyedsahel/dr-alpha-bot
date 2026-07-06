from flask import Blueprint, request

from app.models.service import Service
from app.extensions import db
from app.utils.validators import safe_int

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
            "recovery_days": service.recovery_days,
            "is_active": service.is_active
        })

    return result, 200

@admin_services_bp.route(
    "/services",
    methods=["POST"]
)
def create_service():

    data = request.get_json()

    name = data.get("name")

    if not name:
        return {
            "error": "name is required"
        }, 400

    existing_service = Service.query.filter_by(
        name=name
    ).first()

    if existing_service:
        return {
            "error": "service already exists"
        }, 409

    recovery_days = safe_int(data.get("recovery_days"))

    if recovery_days is None:
        return {
            "error": "recovery_days is required and must be an integer"
        }, 400

    price = safe_int(data.get("price")) if data.get("price") is not None else None

    service = Service(
        name=name,
        price=price,
        description=data.get("description"),
        recovery_days=recovery_days
    )

    db.session.add(service)
    db.session.commit()

    return {
        "message": "service created",
        "service_id": service.id
    }, 201

@admin_services_bp.route(
    "/services/<int:service_id>",
    methods=["PATCH"]
)
def update_service(service_id):

    service = Service.query.get(
        service_id
    )

    if not service:
        return {
            "error": "service not found"
        }, 404

    data = request.get_json()

    if "name" in data:
        existing_service = Service.query.filter_by(
        name=data["name"]
        ).first()

        if existing_service and existing_service.id != service.id:
            return {
                "error": "service name already exists"
            }, 409

        service.name = data["name"]

    if "price" in data:
        service.price = safe_int(data["price"])

    if "description" in data:
        service.description = data["description"]

    if "is_active" in data:
        service.is_active = data["is_active"]
    
    if "recovery_days" in data:
        recovery_days = safe_int(data["recovery_days"])
        if recovery_days is None:
            return {
                "error": "recovery_days must be an integer"
            }, 400
        service.recovery_days = recovery_days

    db.session.commit()

    return {
        "message": "service updated"
    }, 200

@admin_services_bp.route(
    "/services/<int:service_id>",
    methods=["DELETE"]
)
def delete_service(service_id):

    service = Service.query.get(
        service_id
    )

    if not service:
        return {
            "error": "service not found"
        }, 404

    service.is_active = False

    db.session.commit()

    return {
        "message": "service deactivated"
    }, 200