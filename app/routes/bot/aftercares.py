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
            "service_name": aftercare.service_name
        })

    return result, 200

@aftercares_bp.route(
    "/aftercares/<string:service_name>",
    methods=["GET"]
)
def get_aftercare(service_name):

    aftercare = AfterCare.query.filter_by(
        service_name=service_name
    ).first()

    if not aftercare:

        return {
            "error":"aftercare not found"
        },404

    return {
        "id":aftercare.id,
        "service_name":aftercare.service_name,
        "content":aftercare.content
    },200