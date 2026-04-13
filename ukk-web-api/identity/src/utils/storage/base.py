class StorageInterface:
    def upload_file(self, file_path: str, data: bytes, content_type: str, is_public: bool = False, **kwargs) -> dict:
        """
        Upload a file to storage.

        Returns:
            {
                "id": str,          # The storage config ID (e.g. AZURE_1)
                "path": str,        # The saved path (e.g. folder/file.png)
                "base_url": Optional[str]  # Public URL if applicable
            }
        """
        raise NotImplementedError

    def download_file(self, file_path: str, is_public: bool = False, **kwargs) -> bytes:
        raise NotImplementedError

    def delete_file(self, file_path: str, is_public: bool = False, **kwargs):
        raise NotImplementedError
