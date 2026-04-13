from typing import Annotated

from app.auth.oauth2 import get_cred_with_permission
from db.database import get_db
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from utils.repo.queries import BrowseSchema, BulkId, browse_query
from utils.responses import res_success

from .models import Req
from .service import PermissionService

path = 'auth/permissions'
router = APIRouter(prefix=f'/v1/{path}', tags=[path], dependencies=[])

# BROWSE
@router.get('')
def browse(
    browse_queries: Annotated[BrowseSchema, Depends(browse_query)],
    db: Annotated[Session, Depends(get_db)],
    cred: Annotated[dict, Depends(get_cred_with_permission('browse'))],
  ):
  service = PermissionService(db=db, cred=cred)
  data = service.get_index(browse_queries=browse_queries)
  return res_success(data=data)

# READ
@router.get('/{id}')
def browse_id(
    id: int,
    db: Annotated[Session, Depends(get_db)],
    cred: Annotated[dict, Depends(get_cred_with_permission('read'))],
  ):
  service = PermissionService(db=db, cred=cred)
  data = service.get_id(id=id)
  return res_success(data=data)

# CREATE
@router.post('')
def post_create(
    req: Req,
    db: Annotated[Session, Depends(get_db)],
    cred: Annotated[dict, Depends(get_cred_with_permission('create'))],
  ):
  service = PermissionService(db=db, cred=cred)
  data = service.store(req=req)
  return res_success(data=data, db=db)

@router.post('/bulk')
def post_bulk(
  req: list[Req],
  db: Annotated[Session, Depends(get_db)],
  cred: Annotated[dict, Depends(get_cred_with_permission('import'))],
):
  service = PermissionService(db=db, cred=cred)
  data = service.bulk_store(req=req)
  return res_success(data=data, db=db)


# UPDATE
@router.put('/{id}')
def put_update(
    id: int,
    req: Req,
    db: Annotated[Session, Depends(get_db)],
    cred: Annotated[dict, Depends(get_cred_with_permission('update'))],
):
  service = PermissionService(db=db, cred=cred)
  data = service.store(req=req, id=id)
  return res_success(data=data, db=db)

# DELETE & RESTORE
@router.delete('/delete')
def r_delete(
  db: Annotated[Session, Depends(get_db)],
  cred: Annotated[dict, Depends(get_cred_with_permission('delete'))],
  req: BulkId,
  id: int | None = None
):
  service = PermissionService(db=db, cred=cred)
  data = service.delete(req=req, id=id)
  return res_success(data=data, db=db)

@router.delete('/restore')
def r_restore(
  db: Annotated[Session, Depends(get_db)],
  cred: Annotated[dict, Depends(get_cred_with_permission('restore'))],
  req: BulkId,
  id: int | None = None
):
  service = PermissionService(db=db, cred=cred)
  data = service.restore(req=req, id=id)
  return res_success(data=data, db=db)
