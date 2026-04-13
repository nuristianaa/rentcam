from typing import Annotated

from app.auth.oauth2 import get_cred_with_permission
from db.database import get_db
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from utils.repo.queries import BrowseSchema, BulkId, browse_query
from utils.responses import res_success

from .models import Req
from .service import ItemCategoryService

path = "master/item-categories"
router = APIRouter(prefix=f"/v1/{path}", tags=[path], dependencies=[])


# BROWSE
@router.get("")
def browse(
  browse_queries: Annotated[BrowseSchema, Depends(browse_query)],
  db: Annotated[Session, Depends(get_db)],
):
  service = ItemCategoryService(db=db, cred=None)
  data = service.get_index(browse_queries)
  return res_success(data=data)


# READ
@router.get("/{id}")
def browse_id(
  id: int,
  db: Annotated[Session, Depends(get_db)],
  cred: Annotated[dict, Depends(get_cred_with_permission('read'))],
):
  service = ItemCategoryService(db=db, cred=cred)
  data = service.get_id(id)
  return res_success(data=data)


# CREATE
@router.post("")
def post_create(
  req: Req,
  db: Annotated[Session, Depends(get_db)],
  cred: Annotated[dict, Depends(get_cred_with_permission('create'))],
):
  service = ItemCategoryService(db=db, cred=cred)
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
  service = ItemCategoryService(db=db, cred=cred)
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
  service = ItemCategoryService(db=db, cred=cred)
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
  service = ItemCategoryService(db=db, cred=cred)
  data = service.restore(request, id)
  return res_success(data=data, db=db)