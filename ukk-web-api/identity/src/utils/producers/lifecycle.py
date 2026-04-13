from .producer_redis import RedisPool


def startup_queue():
  print("🚀 Queue startup: Redis")
  RedisPool.initialize()
  print("🔌 Redis warm-up started")


def shutdown_queue():
  print("🛑 Queue shutdown")

  pool = RedisPool._pool
  if pool:
    try:
      pool.disconnect()
      print("🔌 Redis pool closed")
    except Exception as e:
      print(f"⚠️ Redis close error: {e}")
    

  print("✅ Queue shutdown complete")
