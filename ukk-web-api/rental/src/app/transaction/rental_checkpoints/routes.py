from typing import Annotated

from app.auth.oauth2 import get_cred_with_permission
from db.database import get_db
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from utils.repo.queries import BrowseSchema, browse_query
from utils.responses import NotFound404, res_success

from .models import RentalCheckpoint, tbl_select
from .repo import RentalCheckpointRepo

path = "transaction/rental-checkpoints"
router = APIRouter(prefix=f"/v1/{path}", tags=[path])


@router.get("")
@router.get("/")
def get_index(
  q: Annotated[BrowseSchema, Depends(browse_query)],
  db: Annotated[Session, Depends(get_db)],
  cred: Annotated[dict, Depends(get_cred_with_permission("browse"))],
  rental_id: str | None = None,
):
  repo = RentalCheckpointRepo(db=db)
  query = db.query(RentalCheckpoint)
  if rental_id:
    query = query.filter(RentalCheckpoint.rental_id == rental_id)
  data = repo.browse(browse_queries=q, model=tbl_select(), query=query)
  return res_success(data=data)


# Semua checkpoint (checkout + checkin) milik sebuah rental
@router.get("/by-rental/{rental_id}")
def get_by_rental(
  rental_id: str,
  db: Annotated[Session, Depends(get_db)],
  cred: Annotated[dict, Depends(get_cred_with_permission("read"))],
):
  repo = RentalCheckpointRepo(db=db)
  data = repo.get_by_rental(rental_id=rental_id)
  return res_success(data=data)


# Detail satu checkpoint berdasarkan ID
@router.get("/{id}")
def get_id(
  id: str,
  db: Annotated[Session, Depends(get_db)],
  cred: Annotated[dict, Depends(get_cred_with_permission("read"))],
):
  row = db.query(RentalCheckpoint).filter(
    RentalCheckpoint.id == id,
    RentalCheckpoint.deleted_at.is_(None),
  ).first()
  if not row:
    raise NotFound404()
  return res_success(data=row)