from flask import Blueprint
from app.models.festival import Festival

festivals_bp = Blueprint("festivals", __name__)


@festivals_bp.route("/festivals", methods=["GET"])
def get_festivals():

    festivals = Festival.query.filter_by(is_active=True).all()

    result = []

    for festival in festivals:
        result.append({
            "id": festival.id,
            "title": festival.title,
            "description": festival.description
        })

    return result, 200