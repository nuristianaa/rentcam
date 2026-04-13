from typing import Annotated

from app.auth.oauth2 import get_cred_with_permission
from db.database import get_db
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from utils.repo.queries import BrowseSchema, BulkId, browse_query
from utils.responses import res_success

from .models import Req, ReqVerify
from .service import PaymentService

path = "transaction/payments"
router = APIRouter(prefix=f"/v1/{path}", tags=[path], dependencies=[])


# BROWSE
@router.get("")
def browse(
  browse_queries: Annotated[BrowseSchema, Depends(browse_query)],
  db: Annotated[Session, Depends(get_db)],
  cred: Annotated[dict, Depends(get_cred_with_permission('browse'))],
):
  service = PaymentService(db=db, cred=cred)
  data = service.get_index(browse_queries)
  return res_success(data=data)


# READ
@router.get("/{id}")
def browse_id(
  id: str,
  db: Annotated[Session, Depends(get_db)],
  cred: Annotated[dict, Depends(get_cred_with_permission('read'))],
):
  service = PaymentService(db=db, cred=cred)
  data = service.get_id(id)
  return res_success(data=data)


# CREATE (customer upload bukti / catat COD)
@router.post("")
def post_create(
  req: Req,
  db: Annotated[Session, Depends(get_db)],
  cred: Annotated[dict, Depends(get_cred_with_permission('create'))],
):
  service = PaymentService(db=db, cred=cred)
  data = service.store(req)
  return res_success(data=data, db=db)


# VERIFY (petugas approve / tolak)
@router.put("/{id}/verify")
def verify(
  id: str,
  req: ReqVerify,
  db: Annotated[Session, Depends(get_db)],
  cred: Annotated[dict, Depends(get_cred_with_permission('update'))],
):
  service = PaymentService(db=db, cred=cred)
  data = service.verify(id=id, req=req)
  return res_success(data=data, db=db)


# DELETE
@router.delete("/delete")
def r_delete(
  db: Annotated[Session, Depends(get_db)],
  cred: Annotated[dict, Depends(get_cred_with_permission('delete'))],
  request: BulkId,
  id: str | None = None,
):
  service = PaymentService(db=db, cred=cred)
  data = service.delete(request, id)
  return res_success(data=data, db=db)