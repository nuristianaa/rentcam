import logging
import os
from logging.handlers import TimedRotatingFileHandler

PARENT_FOLDER = "static_files"
LOG_DIR = os.path.join(PARENT_FOLDER, "logs")
os.makedirs(PARENT_FOLDER, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, "logger_scheduler")

logger_scheduler = logging.getLogger("logger_scheduler")
logger_scheduler.setLevel(logging.INFO)

handler = TimedRotatingFileHandler(
  LOG_FILE, when="D", interval=1, backupCount=30, encoding="utf-8"
)
handler.setLevel(logging.INFO)

formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
handler.setFormatter(formatter)

if not logger_scheduler.handlers:
  logger_scheduler.addHandler(handler)