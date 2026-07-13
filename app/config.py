import os
from dotenv import load_dotenv

load_dotenv()


class Config:

    SECRET_KEY = os.environ.get("SECRET_KEY")
    ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME")
    ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD")
    UPLOAD_FOLDER= os.environ.get("UPLOAD_FOLDER")
    PUBLIC_BASE_URL = os.environ.get("PUBLIC_BASE_URL")

    if not SECRET_KEY or not ADMIN_USERNAME or not ADMIN_PASSWORD or not UPLOAD_FOLDER or not PUBLIC_BASE_URL:
        raise RuntimeError(
            "SECRET_KEY, ADMIN_USERNAME, ADMIN_PASSWORD باید در .env تنظیم شوند"
        )
