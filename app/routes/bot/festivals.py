from flask import Blueprint, url_for
from app.models.festival import Festival

festivals_bp = Blueprint("festivals", __name__)


@festivals_bp.route("/festivals",
    methods=["GET"])
def get_festivals():

    festivals = Festival.query.filter_by(is_active=True).all()
    festivals = Festival.query.all()


    result = []

    for festival in festivals:
        image_url = None
        if festival.image_path:
            image_url = url_for(
                "uploads.uploaded_file",
                filename=f"festivals/{festival.image_path}",
                _external=True
            )
        result.append({
            "id": festival.id,
            "title": festival.title,
            "description": festival.description,
            "image_url": image_url
        })

    return result, 200