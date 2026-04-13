import os
from mimetypes import guess_extension, guess_type

from utils.responses import BadRequest400

from .base import StorageInterface


def get_extension_from_content_type(content_type: str) -> str:
    ext = guess_extension(content_type)
    return ext.lstrip(".") if ext else "bin"


class StaticFilesStorage(StorageInterface):
    def __init__(self, config: dict):
        self.id = config["id"]
        self.folder = config["folder"]
        self.base_url = config["endpoint"]

        if not os.path.isabs(self.folder):
            rental_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
            self.folder = os.path.join(rental_root, self.folder)

        os.makedirs(self.folder, exist_ok=True)

    def upload_file(
        self,
        file_path: str,
        data: bytes,
        content_type: str | None = None,
        is_public: bool = False,  # Ignored for static files
        metadata: dict | None = None,  # Ignored for static files
    ) -> dict:
        if not content_type:
            guessed_type, _ = guess_type(file_path)
            if not guessed_type:
                raise Exception(
                    "Cannot determine content type. Please specify content_type."
                )
            content_type = guessed_type

        ext = get_extension_from_content_type(content_type)
        path = f"{file_path}.{ext}"
        full_path = os.path.join(self.folder, path)

        # Ensure directory exists
        os.makedirs(os.path.dirname(full_path), exist_ok=True)

        with open(full_path, "wb") as f:
            f.write(data)

        result = {
            "id": self.id,
            "path": path,
            "base_url": self.base_url,
        }
        return result

    def download_file(self, file_path: str, is_public: bool = False) -> bytes:
        full_path = os.path.join(self.folder, file_path)
        if not os.path.isfile(full_path):
            raise BadRequest400(f"{file_path} not found")
        with open(full_path, "rb") as f:
            return f.read()

    def delete_file(self, file_path: str, is_public: bool = False) -> dict:
        full_path = os.path.join(self.folder, file_path)
        if os.path.isfile(full_path):
            os.remove(full_path)
            return {"message": f"'{file_path}' deleted successfully"}
        return {"message": f"'{file_path}' does not exist"}
