import os
import uuid

from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {
    "jpg",
    "jpeg",
    "png",
    "webp"
}


def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower()
        in ALLOWED_EXTENSIONS
    )


def save_image(file, upload_folder):

    extension = file.filename.rsplit(".", 1)[1].lower()

    filename = f"{uuid.uuid4()}.{extension}"

    os.makedirs(upload_folder, exist_ok=True)

    path = os.path.join(
        upload_folder,
        secure_filename(filename)
    )

    file.save(path)

    return filename


def delete_image(upload_folder, filename):

    if not filename:
        return

    path = os.path.join(upload_folder, filename)

    if os.path.exists(path):
        os.remove(path)