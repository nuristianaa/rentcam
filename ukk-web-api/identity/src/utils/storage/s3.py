# import boto3
# from mimetypes import guess_type, guess_extension
# from .base import StorageInterface


# def get_extension_from_content_type(content_type: str) -> str:
#     ext = guess_extension(content_type)
#     return ext.lstrip(".") if ext else "bin"


# class S3Storage(StorageInterface):
#     def __init__(self, config: dict):
#         self.id = config["id"]
#         self.bucket = config["bucket"]
#         self.base_url = config.get("base_url")

#         self.client = boto3.client(
#             "s3",
#             aws_access_key_id=config["access_key"],
#             aws_secret_access_key=config["secret_key"],
#             endpoint_url=config.get("endpoint"),
#         )

#     def upload_file(self, file_path: str, data: bytes, content_type: str | None = None, is_public: bool = False, metadata: dict | None = None) -> dict:
#         if not content_type:
#             guessed_type, _ = guess_type(file_path)
#             if not guessed_type:
#                 raise Exception("Cannot determine content type. Please specify content_type.")
#             content_type = guessed_type

#         ext = get_extension_from_content_type(content_type)
#         path = f"{file_path}.{ext}"

#         extra_args = {
#             "ContentType": content_type,
#             "ACL": "public-read" if is_public else "private"
#         }

#         if metadata:
#             extra_args["Metadata"] = metadata # type: ignore

#         self.client.put_object(
#             Bucket=self.bucket,
#             Key=path,
#             Body=data,
#             **extra_args
#         )

#         result = {
#             "id": self.id,
#             "path": path,
#         }

#         if is_public and self.base_url:
#             result["base_url"] = self.base_url

#         return result

#     def download_file(self, file_path: str, is_public: bool = False) -> bytes:
#         obj = self.client.get_object(Bucket=self.bucket, Key=file_path)
#         return obj["Body"].read()

#     def delete_file(self, file_path: str, is_public: bool = False) -> dict:
#         self.client.delete_object(Bucket=self.bucket, Key=file_path)
#         return {"message": f"'{file_path}' deleted successfully"}
