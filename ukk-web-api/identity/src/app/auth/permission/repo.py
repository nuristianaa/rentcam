from sqlalchemy import tuple_
from sqlalchemy.orm import Session
from utils.repo.std_repo import StdRepo

from .models import Permission as Model
from .models import Req


class PermissionRepo(StdRepo):
  def __init__(self, db: Session):
    super().__init__(db, Model)

  def bulk_prepare(self, req: list[Req]):
    keys = [(v.app, v.name) for v in req]
    existing = self.db.query(
      Model
    ).filter(
      tuple_(Model.app, Model.name).in_(keys)
    ).all()
    return {(r.app, r.name): r for r in existing}
