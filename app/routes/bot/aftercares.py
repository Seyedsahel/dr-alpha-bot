from flask import Blueprint

from app.models.aftercare import AfterCare

aftercares_bp = Blueprint(
    "aftercares",
    __name__
)

@aftercares_bp.route(
    "/aftercares",
    methods=["GET"]
)
def get_aftercares():

    aftercares = AfterCare.query.all()

    result = []

    for aftercare in aftercares:

        result.append({
            "id": aftercare.id,
            "service_id": aftercare.service_id,
            "service_name": aftercare.service.name if aftercare.service else None
        })

    return result, 200


@aftercares_bp.route(
    "/aftercares/<int:service_id>",
    methods=["GET"])

def get_aftercare(service_id):

    aftercare = AfterCare.query.filter_by(
        service_id=service_id,
        is_active=True
    ).first()

    if not aftercare:
        return {"error": "aftercare not found"}, 404

    return {
        "id": aftercare.id,
        "service_id": aftercare.service_id,
        "service_name": aftercare.service.name if aftercare.service else None,
        "content": aftercare.content
    }, 200