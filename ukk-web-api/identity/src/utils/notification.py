from pydantic import BaseModel

from utils.producers.publisher import publish

QUEUE = "notif"


class ReqNotif(BaseModel):
  usernames: list[str] | None = None
  app: str | None = None
  title: str | None = None
  description: str | None = None
  path: str | None = None
  type: str | None = None


def send_notif(req: ReqNotif) -> str:
  try:
    publish(QUEUE, req.model_dump())
    return f"{req.title} notif queued"
  except Exception as e:
    print("notif: failed to send notification", str(e))
    return f"{req.title} notif skipped"
