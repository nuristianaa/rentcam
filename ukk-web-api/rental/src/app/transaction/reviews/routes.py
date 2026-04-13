from typing import Annotated

from app.auth.oauth2 import get_cred_with_permission
from db.database import get_db
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from utils.repo.queries import BrowseSchema, BulkId, browse_query
from utils.responses import res_success

from .models import Req, ReqToggleVisible
from .service import ReviewService

path = "transaction/reviews"
router = APIRouter(prefix=f"/v1/{path}", tags=[path], dependencies=[])


# BROWSE (admin)
@router.get("")
def browse(
  browse_queries: Annotated[BrowseSchema, Depends(browse_query)],
  db: Annotated[Session, Depends(get_db)],
  cred: Annotated[dict, Depends(get_cred_with_permission('browse'))],
):
  service = ReviewService(db=db, cred=cred)
  data = service.get_index(browse_queries)
  return res_success(data=data)


# BROWSE BY RENTAL
@router.get("/by-rental/{rental_id}")
def browse_by_rental(
  rental_id: str,
  db: Annotated[Session, Depends(get_db)],
  cred: Annotated[dict, Depends(get_cred_with_permission('read'))],
):
  service = ReviewService(db=db, cred=cred)
  data = service.get_by_rental(rental_id=rental_id)
  return res_success(data=data)


# BROWSE BY ITEM (publik — untuk halaman detail alat)
@router.get("/by-item/{item_id}")
def browse_by_item(
  item_id: int,
  db: Annotated[Session, Depends(get_db)],
):
  service = ReviewService(db=db, cred=None)
  data = service.get_by_item(item_id=item_id)
  return res_success(data=data)


# READ
@router.get("/{id}")
def browse_id(
  id: str,
  db: Annotated[Session, Depends(get_db)],
  cred: Annotated[dict, Depends(get_cred_with_permission('read'))],
):
  service = ReviewService(db=db, cred=cred)
  data = service.get_id(id)
  return res_success(data=data)


# CREATE (customer buat review setelah rental selesai)
@router.post("")
def post_create(
  req: Req,
  db: Annotated[Session, Depends(get_db)],
  cred: Annotated[dict, Depends(get_cred_with_permission('create'))],
):
  service = ReviewService(db=db, cred=cred)
  data = service.store(req)
  return res_success(data=data, db=db)


# TOGGLE VISIBLE (admin sembunyikan / tampilkan review)
@router.put("/{id}/toggle-visible")
def toggle_visible(
  id: str,
  req: ReqToggleVisible,
  db: Annotated[Session, Depends(get_db)],
  cred: Annotated[dict, Depends(get_cred_with_permission('update'))],
):
  service = ReviewService(db=db, cred=cred)
  data = service.toggle_visible(id=id, req=req)
  return res_success(data=data, db=db)


# DELETE
@router.delete("/delete")
def r_delete(
  db: Annotated[Session, Depends(get_db)],
  cred: Annotated[dict, Depends(get_cred_with_permission('delete'))],
  request: BulkId,
  id: str | None = None,
):
  service = ReviewService(db=db, cred=cred)
  data = service.delete(request, id)
  return res_success(data=data, db=db)