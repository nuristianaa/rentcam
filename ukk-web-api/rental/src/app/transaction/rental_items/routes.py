from typing import Annotated

from app.auth.oauth2 import get_cred_with_permission
from db.database import get_db
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from utils.repo.queries import BrowseSchema, browse_query
from utils.responses import res_success

from .service import RentalItemService

path = "transaction/rental-items"
router = APIRouter(prefix=f"/v1/{path}", tags=[path], dependencies=[])


# BROWSE
@router.get("")
def browse(
  browse_queries: Annotated[BrowseSchema, Depends(browse_query)],
  db: Annotated[Session, Depends(get_db)],
  cred: Annotated[dict, Depends(get_cred_with_permission('browse'))],
):
  service = RentalItemService(db=db, cred=cred)
  data = service.get_index(browse_queries)
  return res_success(data=data)


# BROWSE BY RENTAL
@router.get("/by-rental/{rental_id}")
def browse_by_rental(
  rental_id: str,
  db: Annotated[Session, Depends(get_db)],
  cred: Annotated[dict, Depends(get_cred_with_permission('browse'))],
):
  service = RentalItemService(db=db, cred=cred)
  data = service.get_by_rental(rental_id=rental_id)
  return res_success(data=data)


# READ
@router.get("/{id}")
def browse_id(
  id: str,
  db: Annotated[Session, Depends(get_db)],
  cred: Annotated[dict, Depends(get_cred_with_permission('read'))],
):
  service = RentalItemService(db=db, cred=cred)
  data = service.get_id(id)
  return res_success(data=data)