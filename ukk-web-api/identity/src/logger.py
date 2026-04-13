import logging
import os
from logging.handlers import TimedRotatingFileHandler

PARENT_FOLDER = "static_files"
LOG_DIR = os.path.join(PARENT_FOLDER, "logs")
os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE = os.path.join(LOG_DIR, "logger")

logger = logging.getLogger("logger")
logger.setLevel(logging.INFO)

if not logger.handlers:
  handler = TimedRotatingFileHandler(
    LOG_FILE, when="D", interval=1, backupCount=30, encoding="utf-8"
  )
  handler.setLevel(logging.INFO)
  formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
  handler.setFormatter(formatter)
  logger.addHandler(handler)

logger.info("✅ Logger initialized and working.")


# class DedupFilter(logging.Filter):
#   def __init__(self, window_seconds=3600):
#     super().__init__()
#     self.window_seconds = window_seconds
#     self.last_message = None
#     self.last_time = 0

#   def filter(self, record: logging.LogRecord) -> bool:
#     now = time.time()
#     msg = record.getMessage()
#     if msg == self.last_message and (now - self.last_time) < self.window_seconds:
#         return False  # skip duplicate
#     self.last_message = msg
#     self.last_time = now
#     return True

# logger = logging.getLogger("logger")
# logger.setLevel(logging.INFO)

# handler = TimedRotatingFileHandler(
#   LOG_FILE, when="D", interval=1, backupCount=30, encoding="utf-8"
# )
# handler.setLevel(logging.INFO)

# formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
# handler.setFormatter(formatter)

# handler.addFilter(DedupFilter(window_seconds=3600))

# if not logger.handlers:
#   logger.addHandler(handler)
