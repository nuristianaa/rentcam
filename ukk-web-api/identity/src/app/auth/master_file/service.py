
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from utils.helpers.date import currentmillis
from utils.repo.queries import BrowseSchema, BulkId, browse, soft_delete
from utils.responses import BadRequest400, NotFound404
from utils.storage.factory import get_active_storage

from .models import MasterFile as Model
from .models import RequestCreate, tbl_select

module_name = "MasterFile"
storage = get_active_storage()


def create(
  req: RequestCreate, db: Session, cred: dict, file: bytes | None, content_type: str | None = None, filename: str | None = None
):
  try:
    data = Model(
      app=req.app,
      name=req.name,
      description=req.description,
      reference_id=req.reference_id,
      reference_code=req.reference_code,
      module=req.module,
      filetype=content_type,
      is_public=req.is_public,
      filename=filename,
      created_by=cred["username"],
    )
    if file:
      slug = currentmillis()
      file_path = f"{data.app}/{data.module}/{data.reference_code}-{data.name}_{data.reference_id}{slug}"
      is_public = bool(req.is_public)
      path = storage.upload_file(file_path=file_path, data=file, content_type=content_type or '', is_public=is_public)
      data.storage_id = path.get('id', None)
      data.path = path.get('path', None)
      data.base_url = path.get('base_url', None)
    db.add(data)
    db.flush()
    db.refresh(data)
    return data
  except Exception as e:
    raise BadRequest400(str(e), e) from e


def update(
  id: int,
  req: RequestCreate,
  db: Session,
  cred: dict,
  file: bytes | None,
  content_type: str | None = None,
  filename: str | None = None
):
  try:
    username = cred["username"]
    data = db.query(Model).filter(Model.id == id).first()
    if data:
      values: dict = {
        "app": req.app,
        "name": req.name,
        "description": req.description,
        "reference_id": req.reference_id,
        "reference_code": req.reference_code,
        "module": req.module,
        "is_public": req.is_public,
        "updated_by": username,
      }
      if content_type: values['filetype'] = content_type
      if filename: values['filename'] = filename
      is_public = bool(data.is_public)
      if req.delete_file == "true":
        values.update({"path": None})
        if data.path:
          storage.delete_file(file_path=data.path, is_public=is_public)
      elif file:
        if data.path:
          storage.delete_file(file_path=data.path, is_public=is_public)
        slug = currentmillis()
        file_path = f"{req.app}/{req.module}/{req.reference_code}-{req.name}_{req.reference_id}{slug}"
        is_public = bool(req.is_public)
        path = storage.upload_file(file_path=file_path, data=file, content_type=content_type or '', is_public=is_public)
        values['storage_id'] = path.get('id', None)
        values['path'] = path.get('path', None)
        values['base_url'] = path.get('base_url', None)
      db.query(Model).filter(Model.id == id).update(values)
      db.flush()
      db.refresh(data)
      return data
    else:
      raise NotFound404(None, id)
  except IntegrityError as e:
    db.rollback()
    raise BadRequest400(str(e), e) from e


def get_index(browse_queries: BrowseSchema, db: Session):
  """Returns list based on query."""
  try:
    return browse(browse_queries=browse_queries, model=tbl_select, db=db)
  except Exception as e:
    msg = module_name + " get_index: " + str(e)
    raise BadRequest400(msg, e) from e


def get_id(id: int, db: Session):
  """Returns data based on data id."""
  data = db.query(Model).filter(Model.id == id).filter(Model.deleted_at.is_(None)).first()
  return data


def delete(request: BulkId, id: int | None, db: Session, cred: dict):
  if request.id:
    datas = db.query(Model.path, Model.storage_id, Model.is_public).where(Model.id.in_(request.id)).all()
    for data in datas:
      if data and data.storage_id:
        storage_file = get_active_storage(data.storage_id)
        storage_file.delete_file(file_path=data.path, is_public=data.is_public)
  elif id:
    data = db.query(Model.path, Model.storage_id, Model.is_public).where(Model.id == id).first()
    if data and data.storage_id:
      storage_file = get_active_storage(data.storage_id)
      storage_file.delete_file(file_path=data.path, is_public=data.is_public)
  return soft_delete(
    request=request, id=id, db=db, model=Model, cred=cred, type="delete"
  )


def restore(request: BulkId, id: int | None, db: Session, cred: dict):
  return soft_delete(
    request=request, id=id, db=db, model=Model, cred=cred, type="restore"
  )


def get_index_per_module(
  db: Session,
  app: str | None,
  module: str | None,
  reference_id: str | None,
  reference_code: str | None,
):
  try:
    history = []
    items = (
      db.query(Model)
      .where(
        Model.app == app,
        Model.module == module,
        Model.reference_id == reference_id,
        Model.deleted_at.is_(None),
      )
      .order_by(Model.created_at.asc())
      .all()
    )
    if items and len(items) > 0:
      items = [{"id_": v.id, **v.__dict__} for v in items]
    else:
      # history_name = (
      #   db.execute(
      #     select(Model.name)
      #     .where(Model.app == app, Model.module == module)
      #     .group_by(Model.name)
      #   )
      #   .scalars()
      #   .all()
      # )
      history = []
      # history = [
      #   {
      #     "id_": i,
      #     "app": app,
      #     "module": module,
      #     "reference_id": reference_id,
      #     "reference_code": reference_code,
      #     "name": name,
      #     "description": None,
      #     "filename": None,
      #     "filetype": None,
      #     "is_public": False,
      #   }
      #   for i, name in enumerate(history_name, start=1)
      # ]
    return {"items": items, "history": history}
  except Exception as e:
    raise BadRequest400(str(e), e) from e


def get_index_per_reference_id(
  db: Session,
  app: str | None,
  module: str | None,
  reference_id: str | None,
):
  try:
    history = []
    items = (
      db.query(Model)
      .where(
        Model.app == app,
        Model.module == module,
        Model.reference_id == reference_id,
        Model.deleted_at.is_(None),
      )
      .order_by(Model.created_at.asc())
      .all()
    )
    if items and len(items) > 0:
      items = [{"id_": v.id, **v.__dict__} for v in items]

    return {"items": items, "history": history}
  except Exception as e:
    raise BadRequest400(str(e), e) from e
