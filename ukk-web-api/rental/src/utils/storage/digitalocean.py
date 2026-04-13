from mimetypes import guess_extension, guess_type

import boto3

from .base import StorageInterface


def get_extension_from_content_type(content_type: str) -> str:
    extension = guess_extension(content_type)
    if extension:
        return extension.lstrip(".")
    return "bin"


class DigitalOceanStorage(StorageInterface):
    def __init__(self, config: dict):
        self.id = config["id"]  # <-- Store the storage ID (e.g. DO_1)
        self.bucket = config["bucket"]
        self.base_url = config.get("base_url")  # Optional base URL for public access

        self.client = boto3.client(
            "s3",
            region_name=config["region"],
            endpoint_url=config["endpoint"],
            aws_access_key_id=config["access_key"],
            aws_secret_access_key=config["secret_key"],
        )

    def upload_file(
        self,
        file_path: str,
        data: bytes,
        content_type: str | None = None,
        is_public: bool = False,
        metadata: dict | None = None,
    ) -> dict:
        if not content_type:
            guessed_type, _ = guess_type(file_path)
            if not guessed_type:
                raise Exception(
                    "Cannot determine content type. Please specify content_type."
                )
            content_type = guessed_type

        extension = get_extension_from_content_type(content_type)
        path = f"{file_path}.{extension}"

        extra_args = {
            "ACL": "public-read" if is_public else "private",
            "ContentType": content_type,
        }

        if metadata:
            extra_args["Metadata"] = metadata # type: ignore

        self.client.put_object(Bucket=self.bucket, Key=path, Body=data, **extra_args)

        result = {
            "id": self.id,
            "path": path,
        }

        if is_public and self.base_url:
            result["base_url"] = self.base_url

        return result

    def download_file(self, file_path: str, is_public: bool = False) -> bytes:
        obj = self.client.get_object(Bucket=self.bucket, Key=file_path)
        return obj["Body"].read()

    def delete_file(self, file_path: str, is_public: bool = False) -> dict:
        self.client.delete_object(Bucket=self.bucket, Key=file_path)
        return {"message": f"'{file_path}' deleted successfully"}
