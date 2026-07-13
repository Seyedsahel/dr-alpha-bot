from flask import Blueprint, url_for
from app.models.festival import Festival
from flask import request,current_app

festivals_bp = Blueprint("festivals", __name__)


@festivals_bp.route("/festivals",
    methods=["GET"])
def get_festivals():

    festivals = Festival.query.filter_by(is_active=True).all()

    result = []

    for festival in festivals:
        image_url = None
        if festival.image_path:
            image_url = (
                f"{current_app.config['PUBLIC_BASE_URL']}"
                f"/uploads/festivals/{festival.image_path}"
            )
        result.append({
                "id": festival.id,
                "title": festival.title,
                "description": festival.description,
                "image_url": image_url
            })

    return result, 200
