from sqlalchemy.orm import Session
from utils.responses import BadRequest400, NotFound404
from utils.std_service import StdService

from .models import RentalHistory as Model
from .repo import RentalHistoryRepo


class RentalHistoryService(StdService):
  def __init__(self, db: Session, cred: dict | None) -> None:
    self.repo = RentalHistoryRepo(db=db)
    super().__init__(db, cred, self.repo)

  def get_by_rental(self, rental_id: str) -> list:
    try:
      return self.repo.get_by_rental(rental_id=rental_id)
    except Exception as e:
      raise BadRequest400(str(e), e) from e

  def get_id(self, id: str) -> Model:
    try:
      # FIX: delegate ke repo.get_id() — konsisten dengan service lain,
      #      tidak query langsung ke DB dari service layer
      return self.repo.get_id(id=id)
    except NotFound404:
      raise
    except Exception as e:
      raise BadRequest400(str(e), e) from e