from typing import Annotated

from app.auth.oauth2 import get_cred_with_permission
from db.database import get_db
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from utils.repo.queries import BrowseSchema, BulkId, browse_query
from utils.responses import res_success

from .models import Req, ReqCheckpoint, ReqUpdate, ReqUpdateStatus
from .service import RentalService

path = "transaction/rentals"
router = APIRouter(prefix=f"/v1/{path}", tags=[path], dependencies=[])


# BROWSE
@router.get("")
def browse(
  browse_queries: Annotated[BrowseSchema, Depends(browse_query)],
  db: Annotated[Session, Depends(get_db)],
  cred: Annotated[dict, Depends(get_cred_with_permission("browse"))],
):
  service = RentalService(db=db, cred=cred)
  data = service.get_index(browse_queries)
  return res_success(data=data)


# READ
@router.get("/{id}")
def browse_id(
  id: str,
  db: Annotated[Session, Depends(get_db)],
  cred: Annotated[dict, Depends(get_cred_with_permission("read"))],
):
  service = RentalService(db=db, cred=cred)
  data = service.get_id(id)
  return res_success(data=data)


# CREATE
@router.post("")
def post_create(
  req: Req,
  db: Annotated[Session, Depends(get_db)],
  cred: Annotated[dict, Depends(get_cred_with_permission("create"))],
):
  service = RentalService(db=db, cred=cred)
  data = service.store(req)
  return res_success(data=data, db=db)


# UPDATE FULL
@router.put("/{id}")
def update(
  id: str,
  req: ReqUpdate,
  db: Annotated[Session, Depends(get_db)],
  cred: Annotated[dict, Depends(get_cred_with_permission("update"))],
):
  service = RentalService(db=db, cred=cred)
  data = service.update(id=id, req=req)
  return res_success(data=data, db=db)


# UPDATE STATUS (menunggu_bayar → menunggu_verif → diproses → aktif → selesai / dibatalkan)
@router.put("/{id}/status")
def update_status(
  id: str,
  req: ReqUpdateStatus,
  db: Annotated[Session, Depends(get_db)],
  cred: Annotated[dict, Depends(get_cred_with_permission("update"))],
):
  service = RentalService(db=db, cred=cred)
  data = service.update_status(id=id, req=req)
  return res_success(data=data, db=db)


# CHECKOUT — petugas menyerahkan alat ke customer, status diproses → aktif
@router.post("/{id}/checkout")
def checkout(
  id: str,
  req: ReqCheckpoint,
  db: Annotated[Session, Depends(get_db)],
  cred: Annotated[dict, Depends(get_cred_with_permission("update"))],
):
  service = RentalService(db=db, cred=cred)
  data = service.checkout(id=id, req=req)
  return res_success(data=data, db=db)


# CHECKIN — petugas menerima alat kembali dari customer, status aktif → selesai
@router.post("/{id}/checkin")
def checkin(
  id: str,
  req: ReqCheckpoint,
  db: Annotated[Session, Depends(get_db)],
  cred: Annotated[dict, Depends(get_cred_with_permission("update"))],
):
  service = RentalService(db=db, cred=cred)
  data = service.checkin(id=id, req=req)
  return res_success(data=data, db=db)


# DELETE
@router.delete("/delete")
def r_delete(
  db: Annotated[Session, Depends(get_db)],
  cred: Annotated[dict, Depends(get_cred_with_permission("delete"))],
  request: BulkId,
  id: str | None = None,
):
  service = RentalService(db=db, cred=cred)
  data = service.delete(request, id)
  return res_success(data=data, db=db)


# RESTORE
@router.delete("/restore")
def r_restore(
  db: Annotated[Session, Depends(get_db)],
  cred: Annotated[dict, Depends(get_cred_with_permission("restore"))],
  request: BulkId,
  id: str | None = None,
):
  service = RentalService(db=db, cred=cred)
  data = service.restore(request, id)
  return res_success(data=data, db=db)