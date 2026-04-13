# limiter.py
import asyncio
import time
from collections import defaultdict


class LocalLimiter:
  def __init__(self, rate: float, per: int):
    self.rate = rate  # number of requests
    self.per = per    # time window (seconds)
    self.allowance = defaultdict(lambda: rate)
    self.last_check = defaultdict(time.monotonic)
    self.lock = asyncio.Lock()

  async def check(self, key: str = 'all') -> bool:
    async with self.lock:
      current = time.monotonic()
      time_passed = current - self.last_check[key]
      self.last_check[key] = current

      self.allowance[key] += time_passed * (self.rate / self.per)
      if self.allowance[key] > self.rate:
        self.allowance[key] = self.rate

      if self.allowance[key] < 1.0:
        return False  # blocked
      else:
        self.allowance[key] -= 1.0
        return True  # allowed
