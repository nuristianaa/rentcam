import json

from config import getenv
from .producer_redis import RedisPool

STREAM_TYPE = getenv("STREAM_QUEUE_TYPE", "redis").lower()


def publish(queue: str, payload: dict | list | str):
  try:
    client = RedisPool.get_client()
    message = payload if isinstance(payload, str) else json.dumps(payload)
    client.xadd(queue, {"data": message})
  except Exception as e:
    print("redis: ", e)
    raise Exception("Your queue services is not running.")
  print(f"[📤 Sent queue redis] {queue}")
  return True