from flask import Blueprint

from app.models.faq import FAQ

faqs_bp = Blueprint(
    "faqs",
    __name__
)

@faqs_bp.route(
    "/faqs",
    methods=["GET"]
)
def get_faqs():

    faqs = FAQ.query.filter_by(
        is_active=True
    ).all()

    result = []

    for faq in faqs:

        result.append({
            "id": faq.id,
            "question": faq.question,
            "answer": faq.answer
        })

    return result, 200