import asyncio
from queue import Queue

from db.database import LogAsyncSession
from sqlalchemy import insert

from .models import AuditTrail as Model

AUDIT_QUEUE = Queue()
BATCH_SECONDS = 10

async def flush_audit_logs():
  while True:
    await asyncio.sleep(BATCH_SECONDS)
    batch = []

    while not AUDIT_QUEUE.empty():
      batch.append(AUDIT_QUEUE.get())
    
    print(batch)
    if batch and len(batch):
      async with LogAsyncSession() as db:
        try:
          await db.execute(insert(Model).values(batch))
          await db.commit()
          print(f"✅ Flushed {len(batch)} audit logs")
        except Exception as e:
          await db.rollback()
          print(f"❌ Failed to flush logs: {e}")