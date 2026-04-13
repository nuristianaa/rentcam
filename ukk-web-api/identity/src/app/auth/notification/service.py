from datetime import datetime, timedelta

from sqlalchemy.orm import Session
from utils.repo.queries import BrowseSchema
from utils.repo.std_repo import StdRepo
from utils.responses import BadRequest400

from .models import Notification as Model
from .models import PushSubscription, SubscribeReq, tbl_select


def get_index(browse_queries: BrowseSchema, db: Session):
  """Returns list based on query."""
  try:
    repo = StdRepo(db=db, model=Model)
    return repo.browse(browse_queries=browse_queries, model=tbl_select)
  except Exception as e:
    raise BadRequest400(str(e), e)


def get_id(id: int|str, db: Session):
  """Returns data based on data id."""
  db.query(Model).where(Model.id == id).update({Model.is_read: True})
  db.commit()
  return db.query(Model).where(Model.id == id).where(Model.deleted_at.is_(None)).first()


def store_subscriber(req: SubscribeReq, db: Session):
  if req.subscription is None: raise BadRequest400('Subscription is null')
  try:
    # Clear old subs | older than 30 days
    thirty_days_ago = datetime.now() - timedelta(days=30)
    db.query(PushSubscription).where(PushSubscription.created_at <= thirty_days_ago).delete()
    db.flush()

    existing = db.query(PushSubscription).where(PushSubscription.endpoint == req.subscription.endpoint).first()

    if not existing:
      sub = PushSubscription(
        user_id=req.user_id,
        username=req.username,
        endpoint=req.subscription.endpoint,
        p256dh=req.subscription.keys.p256dh if req.subscription.keys else '',
        auth=req.subscription.keys.auth if req.subscription.keys else '',
      )
      db.add(sub)
      db.commit()
      db.refresh(sub)
      return sub
    return existing
  except Exception as e:
    raise BadRequest400(str(e), e)
