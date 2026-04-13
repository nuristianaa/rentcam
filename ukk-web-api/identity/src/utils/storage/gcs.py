# from google.cloud import storage
# from mimetypes import guess_extension, guess_type
# from .base import StorageInterface


# def get_extension_from_content_type(content_type: str) -> str:
#     ext = guess_extension(content_type)
#     return ext.lstrip(".") if ext else "bin"


# class GCSStorage(StorageInterface):
#     def __init__(self, config: dict):
#         self.id = config["id"]
#         self.bucket_name = config["bucket"]
#         self.base_url = config.get("base_url")

#         self.client = storage.Client.from_service_account_json(config["credentials_json"])
#         self.bucket = self.client.get_bucket(self.bucket_name)

#     def upload_file(self, file_path: str, data: bytes, content_type: str | None = None, is_public: bool = False, metadata: dict | None = None) -> dict:
#         if not content_type:
#             guessed_type, _ = guess_type(file_path)
#             if not guessed_type:
#                 raise Exception("Cannot determine content type. Please specify content_type.")
#             content_type = guessed_type

#         ext = get_extension_from_content_type(content_type)
#         path = f"{file_path}.{ext}"

#         blob = self.bucket.blob(path)
#         blob.metadata = metadata or {}
#         blob.upload_from_string(data, content_type=content_type)

#         if is_public:
#             blob.make_public()

#         result = {
#             "id": self.id,
#             "path": path,
#         }

#         if is_public and self.base_url:
#             result["base_url"] = self.base_url

#         return result

#     def download_file(self, file_path: str, is_public: bool = False) -> bytes:
#         blob = self.bucket.blob(file_path)
#         return blob.download_as_bytes()

#     def delete_file(self, file_path: str, is_public: bool = False) -> dict:
#         blob = self.bucket.blob(file_path)
#         blob.delete()
#         return {"message": f"'{file_path}' deleted successfully"}