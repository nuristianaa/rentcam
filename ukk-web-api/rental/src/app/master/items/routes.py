from datetime import date, timedelta
from typing import Annotated

from app.auth.oauth2 import get_cred_with_permission
from db.database import get_db
from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.orm import Session
from utils.repo.queries import BrowseSchema, BulkId, browse_query
from utils.responses import res_success
from utils.uploader.upload_files import Uploader

from .models import Item, Req
from .service import ItemService

path = "master/items"
router = APIRouter(prefix=f"/v1/{path}", tags=[path], dependencies=[])


# BROWSE
@router.get("")
def browse(
  browse_queries: Annotated[BrowseSchema, Depends(browse_query)],
  db: Annotated[Session, Depends(get_db)],
):
  service = ItemService(db=db, cred=None)
  data = service.get_index(browse_queries)
  return res_success(data=data)


# UPLOAD FILES — harus di atas /{id} biar ga ketangkep sebagai id
@router.post("/upload-files")
async def upload_files(
  request: Request,
  db: Annotated[Session, Depends(get_db)],
  cred: Annotated[dict, Depends(get_cred_with_permission('create'))],
):
  service = Uploader(db=db, model=Item, module_name=path)
  data = await service.upload_files(request=request, column="images")
  return data


# READ — letakkan SETELAH semua route statis
@router.get("/{id}")
def browse_id(
  id: int,
  db: Annotated[Session, Depends(get_db)],
):
  service = ItemService(db=db, cred=None)
  data = service.get_id(id)
  return res_success(data=data)


@router.get("/{id}/availability")
def get_availability(
  id: int,
  db: Annotated[Session, Depends(get_db)],
  start_date: Annotated[date | None, Query()] = None,
  end_date: Annotated[date | None, Query()] = None,
):
  today = date.today()
  start_date = start_date or today
  end_date = end_date or (start_date + timedelta(days=13))
  service = ItemService(db=db, cred=None)
  data = service.get_availability(id, start_date, end_date)
  return res_success(data=data)


# CREATE
@router.post("")
def post_create(
  req: Req,
  db: Annotated[Session, Depends(get_db)],
  cred: Annotated[dict, Depends(get_cred_with_permission('create'))],
):
  service = ItemService(db=db, cred=cred)
  data = service.store(req)
  return res_success(data=data, db=db)


# UPDATE
@router.put("/{id}")
def put_update(
  id: int,
  req: Req,
  db: Annotated[Session, Depends(get_db)],
  cred: Annotated[dict, Depends(get_cred_with_permission('update'))],
):
  service = ItemService(db=db, cred=cred)
  data = service.store(req=req, id=id)
  return res_success(data=data, db=db)


# DELETE
@router.delete("/delete")
def r_delete(
  db: Annotated[Session, Depends(get_db)],
  cred: Annotated[dict, Depends(get_cred_with_permission('delete'))],
  request: BulkId,
  id: int | None = None,
):
  service = ItemService(db=db, cred=cred)
  data = service.delete(request, id)
  return res_success(data=data, db=db)


# RESTORE
@router.delete("/restore")
def r_restore(
  db: Annotated[Session, Depends(get_db)],
  cred: Annotated[dict, Depends(get_cred_with_permission('restore'))],
  request: BulkId,
  id: int | None = None,
):
  service = ItemService(db=db, cred=cred)
  data = service.restore(request, id)
  return res_success(data=data, db=db)