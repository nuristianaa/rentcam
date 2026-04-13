from typing import Annotated

from app.auth.oauth2 import get_cred_with_permission
from db.database import get_db
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from utils.repo.queries import BrowseSchema, browse_query
from utils.responses import res_success

from app.transaction.rentals.service import RentalService
from .service import RentalHistoryService

path = "transaction/rental-histories"
router = APIRouter(prefix=f"/v1/{path}", tags=[path])


@router.get("")
@router.get("/")
def get_index(
  q: Annotated[BrowseSchema, Depends(browse_query)],
  db: Annotated[Session, Depends(get_db)],
  cred: Annotated[dict, Depends(get_cred_with_permission("browse"))],
):
  service = RentalService(db=db, cred=cred)
  data = service.get_index(browse_queries=q)
  return res_success(data=data)


# Semua history sebuah rental
@router.get("/by-rental/{rental_id}")
def get_by_rental(
  rental_id: str,
  db: Annotated[Session, Depends(get_db)],
  cred: Annotated[dict, Depends(get_cred_with_permission("read"))],
):
  service = RentalHistoryService(db=db, cred=cred)
  data = service.get_by_rental(rental_id)
  return res_success(data=data)


# Detail satu history
@router.get("/{id}")
def get_id(
  id: str,
  db: Annotated[Session, Depends(get_db)],
  cred: Annotated[dict, Depends(get_cred_with_permission("read"))],
):
  service = RentalHistoryService(db=db, cred=cred)
  data = service.get_id(id)
  return res_success(data=data)