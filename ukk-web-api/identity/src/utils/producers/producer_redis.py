import threading

import redis

from config import getenv
from ..responses import BadRequest400

REDIS_HOST = getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(getenv("REDIS_PORT", "6379"))
REDIS_DB = int(getenv("REDIS_DB", "0"))
REDIS_PASSWORD = getenv("REDIS_PASSWORD", "None")

POOL_SIZE = 10


class RedisPool:
  _pool = None
  _lock = threading.RLock()
  _initialized = False

  # ---------------------------------------------------
  # Connection Pool
  # ---------------------------------------------------
  @classmethod
  def _create_pool(cls):
    try:
      print("🔌 Connecting to Redis...")
      pool = redis.ConnectionPool(
        host=REDIS_HOST,
        port=REDIS_PORT,
        db=REDIS_DB,
        password=REDIS_PASSWORD,
        max_connections=POOL_SIZE,
        decode_responses=True,
        socket_connect_timeout=2,
        socket_timeout=2,
        retry_on_timeout=True,
      )
      # test connection
      r = redis.Redis(connection_pool=pool)
      r.ping()
      print("✅ Redis connected")
      return pool
    except Exception as e:
      raise BadRequest400(f"Redis connection failed: {e}")

  @classmethod
  def get_client(cls) -> redis.Redis:
    with cls._lock:
      if cls._pool is None:
        cls._pool = cls._create_pool()
      return redis.Redis(connection_pool=cls._pool)

  # ---------------------------------------------------
  # Warm-up
  # ---------------------------------------------------
  @classmethod
  def initialize(cls):
    if cls._initialized:
      return
    cls._initialized = True
    threading.Thread(target=cls._warmup, daemon=True).start()

  @classmethod
  def _warmup(cls):
    try:
      print("🚀 Redis warm-up started...")
      client = cls.get_client()
      client.ping()
      print("🔥 Redis warm-up completed!")
    except Exception as e:
      print(f"❌ Redis warm-up failed: {e}")
