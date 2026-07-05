from datetime import datetime, timedelta, timezone

import jwt

from flask import current_app


def generate_token(username):

    payload = {
        "username": username,
        "exp": datetime.now(timezone.utc) + timedelta(hours=24)
    }

    return jwt.encode(
        payload,
        current_app.config["SECRET_KEY"],
        algorithm="HS256"
    )


def verify_token(token):

    try:
        return jwt.decode(
            token,
            current_app.config["SECRET_KEY"],
            algorithms=["HS256"]
        )

    except jwt.ExpiredSignatureError:
        return None

    except jwt.InvalidTokenError:
        return None