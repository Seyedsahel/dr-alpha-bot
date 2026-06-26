from flask import Blueprint, request, current_app, url_for
from app.extensions import db
from app.models.festival import Festival
from app.utils.file_handler import (
    allowed_file,
    save_image,
    delete_image
)
import os

admin_festivals_bp = Blueprint("admin_festivals", __name__)


@admin_festivals_bp.route("/festivals",
    methods=["GET"])
def get_festivals():

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
            "image_url": image_url,
            "is_active": festival.is_active,
            "created_at": festival.created_at
        })

    return result, 200

@admin_festivals_bp.route("/festivals", 
    methods=["POST"])
def create_festival():


    title = request.form.get("title")
    description = request.form.get("description")
    image = request.files.get("image")


    if not title or not description:
        return {"error": "title and description are required"}, 400

    if image:
        if not allowed_file(image.filename):
            return {
                "error": "invalid image format"
            },400

        filename = save_image(
            image,
            os.path.join(
                current_app.config["UPLOAD_FOLDER"],
                "festivals"
            )
        )
    else:
        filename = None

    festival = Festival(
        title=title,
        description=description,
        image_path=filename
    )

    db.session.add(festival)
    db.session.commit()

    return {
        "message": "festival created",
        "festival_id": festival.id
    }, 201

@admin_festivals_bp.route("/festivals/<int:festival_id>",
    methods=["PATCH"])
def update_festival(festival_id):

    festival = Festival.query.get(festival_id)

    if not festival:
        return {"error": "festival not found"}, 404

    title = request.form.get("title")
    description = request.form.get("description")
    is_active = request.form.get("is_active")

    if title:
        festival.title = title

    if description:
        festival.description = description


    image = request.files.get("image")
    if image:
        if not allowed_file(image.filename):
            return {
                "error": "invalid image format"
            },400
        delete_image(
            festival.image_path,
            os.path.join(
                current_app.config["UPLOAD_FOLDER"],
                "festivals"
            )
        )
        filename = save_image(
            image,
            os.path.join(
                current_app.config["UPLOAD_FOLDER"],
                "festivals"
            )
        )
        festival.image_path = filename


    if is_active is not None:
        festival.is_active = is_active.lower() == "true"

    db.session.commit()

    return {"message": "festival updated"}, 200

@admin_festivals_bp.route("/festivals/<int:festival_id>",
    methods=["DELETE"])
def delete_festival(festival_id):

    festival = Festival.query.get(festival_id)

    if not festival:
        return {"error": "festival not found"}, 404
    upload_folder = os.path.join(
                current_app.config["UPLOAD_FOLDER"],
                "festivals"
            ) 
    if festival.image_path:
        delete_image(
            upload_folder,
            festival.image_path,
        )
    festival.image_path = None
    festival.is_active = False

    db.session.commit()

    return {"message": "festival deactivated"}, 200