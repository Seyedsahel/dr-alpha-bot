from flask import Blueprint, request

from app.extensions import db
from app.models.faq import FAQ

admin_faqs_bp = Blueprint(
    "admin_faqs",
    __name__
)

@admin_faqs_bp.route(
    "/faqs",
    methods=["GET"]
)
def get_faqs():

    faqs = FAQ.query.all()

    result = []

    for faq in faqs:

        result.append({
            "id": faq.id,
            "question": faq.question,
            "answer": faq.answer,
            "is_active": faq.is_active
        })

    return result, 200

@admin_faqs_bp.route(
    "/faqs",
    methods=["POST"]
)
def create_faq():

    data = request.get_json()

    question = data.get("question")
    answer = data.get("answer")

    if not question or not answer:

        return {
            "error": "question and answer are required"
        }, 400

    faq = FAQ(
        question=question,
        answer=answer
    )

    db.session.add(faq)
    db.session.commit()

    return {
        "message": "faq created",
        "faq_id": faq.id
    }, 201

@admin_faqs_bp.route(
    "/faqs/<int:faq_id>",
    methods=["PATCH"]
)
def update_faq(faq_id):

    faq = FAQ.query.get(faq_id)

    if not faq:

        return {
            "error": "faq not found"
        }, 404

    data = request.get_json()

    if "question" in data:
        faq.question = data["question"]

    if "answer" in data:
        faq.answer = data["answer"]

    if "is_active" in data:
        faq.is_active = data["is_active"]

    db.session.commit()

    return {
        "message": "faq updated"
    }, 200

@admin_faqs_bp.route(
    "/faqs/<int:faq_id>",
    methods=["DELETE"]
)
def delete_faq(faq_id):

    faq = FAQ.query.get(faq_id)

    if not faq:

        return {
            "error": "faq not found"
        }, 404

    faq.is_active = False

    db.session.commit()

    return {
        "message": "faq deactivated"
    }, 200