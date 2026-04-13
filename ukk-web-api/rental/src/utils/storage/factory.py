import json
import os

from config.config import getenv
from pydantic import BaseModel
from utils.responses import BadRequest400

from .base import StorageInterface
from .static_file import StaticFilesStorage


class Settings(BaseModel):
    active_storage_id: str = getenv("ACTIVE_STORAGE_ID", "AZURE_1")
    storage_config_file: str = getenv("STORAGE_CONFIG_FILE", "storage_config.json")


settings = Settings()

# --- Tentukan root project berdasarkan lokasi factory.py ---
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../'))  # identity/
storage_config_path = os.path.join(root_dir, settings.storage_config_file)

if not os.path.exists(storage_config_path):
    raise BadRequest400(
        f"Active storage config not found. Tried path: {storage_config_path}"
    )

# --- Load storage config ---
with open(storage_config_path, 'r', encoding='utf-8') as f:
    storage_config: dict[str, list[dict]] = json.load(f)


def get_active_storage(storage_id: str | None = None) -> StorageInterface:
    """
    Return instance of StorageInterface based on ID (e.g. STATIC_1).
    """
    storage_id = storage_id.upper() if storage_id else settings.active_storage_id

    # --- Cari storage sesuai ID ---
    for storage_type, configs in storage_config.items():
        for cfg in configs:
            if cfg["id"].upper() == storage_id:
                match storage_type.lower():
                    case "static_file":
                        return StaticFilesStorage(cfg)

    # --- fallback ke storage pertama jika ID tidak ditemukan ---
    for storage_type, configs in storage_config.items():
        if not configs:
            continue
        cfg = configs[0]
        match storage_type.lower():
            case "static_file":
                return StaticFilesStorage(cfg)

    raise BadRequest400(f"Active storage config not found for ID: {storage_id}")
