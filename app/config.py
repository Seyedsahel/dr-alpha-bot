import os
from dotenv import load_dotenv

load_dotenv()


class Config:

    SECRET_KEY = os.environ.get("SECRET_KEY")
    ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME")
    ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD")

    if not SECRET_KEY or not ADMIN_USERNAME or not ADMIN_PASSWORD:
        raise RuntimeError(
            "SECRET_KEY, ADMIN_USERNAME, ADMIN_PASSWORD باید در .env تنظیم شوند"
        )