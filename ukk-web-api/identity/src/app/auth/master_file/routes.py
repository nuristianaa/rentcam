import io
import mimetypes
from typing import Annotated

from app.auth.oauth2 import check_jwt, get_cred_base
from db.database import get_db
from fastapi import APIRouter, Depends, File, Query, UploadFile
from fastapi.responses import StreamingResponse
from PIL import Image, ImageDraw, ImageFont
from sqlalchemy.orm import Session
from utils.repo.queries import BrowseSchema, BulkId, browse_query
from utils.responses import BadRequest400, Forbidden403, NotFound404, res_success
from utils.storage.factory import get_active_storage

from .models import ModeEnum, RequestCreate
from .service import (
  create,
  delete,
  get_id,
  get_index,
  get_index_per_module,
  get_index_per_reference_id,
  restore,
  update,
)

path = "auth/master-files"
router = APIRouter(prefix=f"/v1/{path}", tags=[path], dependencies=[])
permission = True
MAX_MB_FILE = 50

# Create visible NA image
def generate_na_image_bytes():
  size=(200, 100)
  # Gray background
  img = Image.new("RGB", size, (200, 200, 200))
  draw = ImageDraw.Draw(img)
  text = "N/A"
  try: font = ImageFont.truetype("DejaVuSans-Bold.ttf", 70)
  except: font = ImageFont.load_default()
  # Center the text
  bbox = draw.textbbox((0, 0), text, font=font)
  text_w, text_h = bbox[2] - bbox[0], bbox[3] - bbox[1]
  x = (size[0] - text_w) // 2
  y = (size[1] - text_h) // 2
  draw.text((x, y), text, fill=(0, 0, 0), font=font)
  buf = io.BytesIO()
  img.save(buf, format="PNG")
  return buf.getvalue()

NA_IMAGE_BYTES = generate_na_image_bytes()


@router.get("/download")
def download_file(
  cred: Annotated[dict, Depends(get_cred_base)],
  path: str,
  mode: ModeEnum = Query(default=ModeEnum.private),
  storage_id: str | None = None
) -> StreamingResponse:
  try:
    storage = get_active_storage(storage_id=storage_id)
    is_public = bool(mode == ModeEnum.public)
    file_data = storage.download_file(file_path=path, is_public=is_public)
    mime_type, _ = mimetypes.guess_type(path)
    mime_type = mime_type or "application/octet-stream"
    return StreamingResponse(
      iter([file_data]),
      media_type=mime_type,
      headers={"Content-Disposition": f"inline; filename={path}"}
    )
  except Exception:
    raise NotFound404('File not found')


@router.get("/view")
def view_file(
  token: str,
  path: str,
  mode: ModeEnum = Query(default=ModeEnum.private),
  storage_id: str | None = None
) -> StreamingResponse:
  try:
    if check_jwt(token):
      storage = get_active_storage(storage_id=storage_id)
      is_public = bool(mode == ModeEnum.public)
      file_data = storage.download_file(file_path=path, is_public=is_public)
      mime_type, _ = mimetypes.guess_type(path)
      mime_type = mime_type or "application/octet-stream"
      return StreamingResponse(
        iter([file_data]),
        media_type=mime_type,
        headers={"Content-Disposition": f"inline; filename={path}"}
      )
    else:
      raise Forbidden403('Invalid token')
  except Exception:
    return StreamingResponse(
      io.BytesIO(NA_IMAGE_BYTES),
      media_type="image/png",
      headers={"Content-Disposition": "inline; filename=NA.png"}
    )


# BROWSE
@router.get("")
def browse(
  browse_queries: Annotated[BrowseSchema, Depends(browse_query)],
  db: Annotated[Session, Depends(get_db)],
  cred: Annotated[dict, Depends(get_cred_base)],
  get_previous_list: bool = False,
  per_reference_id: bool = False,
  app: str|None = None,
  module: str|None = None,
  reference_id: str|None = None,
  reference_code: str|None = None,
):
  if per_reference_id:
    data = get_index_per_reference_id(db, app, module, reference_id)
    return res_success(data=data)
  if get_previous_list: # noqa SIM108
    data = get_index_per_module(db, app, module, reference_id, reference_code)
  else:
    data = get_index(browse_queries, db)
  return res_success(data=data)


# READ
@router.get("/{id}")
def browse_id(
  id: int,
  db: Annotated[Session, Depends(get_db)],
  cred: Annotated[dict, Depends(get_cred_base)],
):
  data = get_id(id, db)
  return res_success(data=data)


# CREATE & UPDATE
@router.post("")
async def post_create(
  db: Annotated[Session, Depends(get_db)],
  cred: Annotated[dict, Depends(get_cred_base)],
  file: UploadFile | None = File(None),
  req: RequestCreate = Depends()
):
  contents = None
  content_type = None
  filename = None
  if file:
    contents = await file.read()
    filesize = len(contents)
    max_size = MAX_MB_FILE * 1024 * 1024
    if filesize > max_size: raise BadRequest400(f"Max filesize: {MAX_MB_FILE} Mb!")
    if file.content_type: content_type = file.content_type
    filename = file.filename
  data = create(req, db, cred, contents, content_type, filename)
  return res_success(data=data, db=db)


# UPDATE
@router.post("/{id}")
async def post_update(
  db: Annotated[Session, Depends(get_db)],
  cred: Annotated[dict, Depends(get_cred_base)],
  id: int,
  file: UploadFile | None = File(None),
  req: RequestCreate = Depends()
):
  contents = None
  content_type = None
  filename = None
  if file:
    contents = await file.read()
    filesize = len(contents)
    max_size = MAX_MB_FILE * 1024 * 1024
    if filesize > max_size: raise BadRequest400(f"Max filesize: {10} Mb!")
    if file.content_type: content_type = file.content_type
    filename = file.filename
  data = update(id, req, db, cred, contents, content_type, filename)
  return res_success(data=data, db=db)


# DELETE & RESTORE
@router.delete("/delete")
def r_delete(
  db: Annotated[Session, Depends(get_db)],
  cred: Annotated[dict, Depends(get_cred_base)],
  request: BulkId,
  id: int | None = None
):
  data = delete(request, id, db, cred)
  return res_success(data=data, db=db)


@router.delete("/restore")
def r_restore(
  db: Annotated[Session, Depends(get_db)],
  cred: Annotated[dict, Depends(get_cred_base)],
  request: BulkId,
  id: int | None = None
):
  data = restore(request, id, db, cred)
  return res_success(data=data, db=db)
