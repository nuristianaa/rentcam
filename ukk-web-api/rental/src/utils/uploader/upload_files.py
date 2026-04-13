from typing import Any

from fastapi import Request
from sqlalchemy import select, update
from sqlalchemy.orm import Session
from sqlalchemy.orm.attributes import InstrumentedAttribute
from utils.responses import BadRequest400
from utils.storage.factory import get_active_storage

storage = get_active_storage()


class Uploader:
  def __init__(self, db: Session, model: Any, module_name: str) -> None:
    self.db = db
    self.model = model
    self.module_name = module_name

  async def upload_files(
    self,
    request: Request,
    column: str = "images",  # column name for files on table module, default "images"
  ):
    try:
      form = await request.form()

      order = form.getlist("order[]")
      delete_ids = form.getlist("delete_ids[]")

      colsize_map = {}
      for key, value in form.multi_items():
        if key.startswith("colSize_"):
          tid = key.replace("colSize_", "")
          colsize_map[tid] = int(value)  # type: ignore

      remark_map = {}
      for key, value in form.multi_items():
        if key.startswith("remark_"):
          tid = key.replace("remark_", "")
          remark_map[tid] = value if value not in (None, "", "undefined") else None

      description_map = {}
      for key, value in form.multi_items():
        if key.startswith("description_"):
          tid = key.replace("description_", "")
          description_map[tid] = value if value not in (None, "", "undefined") else None

      maxheight_map = {}
      for key, value in form.multi_items():
        if key.startswith("maxHeight_"):
          tid = key.replace("maxHeight_", "")
          maxheight_map[tid] = int(value)  # type: ignore

      new_files = {}
      for key, value in form.multi_items():
        if key.startswith("file_"):
          tempId = key.replace("file_", "")
          content = await value.read()  # type: ignore
          new_files[tempId] = {
            "file": content,
            "content_type": value.content_type,  # type: ignore
          }

      req_id = form.get("detail_id") if form.get("detail_id") else form.get("id")
      data = await self.upload_files_id_based(
        req_id=req_id,  # type: ignore
        req_code=form.get("code"),  # type: ignore
        order=order,  # type: ignore
        delete_ids=delete_ids,  # type: ignore
        new_files=new_files,
        colsize_map=colsize_map,
        remark_map=remark_map,
        description_map=description_map,
        maxheight_map=maxheight_map,
        column=column,
      )

      return data
    except Exception as e:
      raise BadRequest400(str(e), e) from e

  async def upload_files_id_based(
    self,
    req_id: str | None = None,
    req_code: str | None = None,
    order: list[str] | None = None,
    delete_ids: list[str] | None = None,
    new_files: dict | None = None,
    colsize_map: dict | None = None,
    description_map: dict | None = None,
    remark_map: dict | None = None,
    maxheight_map: dict | None = None,
    column: str = "images",
  ):
    column_attr = self._resolve_column(column)

    base_path = f"project_management/{self.module_name}/{req_code}-{req_id}"

    order = order or []
    delete_ids = delete_ids or []
    new_files = new_files or {}
    colsize_map = colsize_map or {}
    remark_map = remark_map or {}
    description_map = description_map or {}
    maxheight_map = maxheight_map or {}

    current_data = self.db.execute(select(column_attr).where(self.model.id == req_id, self.model.deleted_at.is_(None))).scalar_one_or_none()
    if not current_data:
      current_data = {}
    else:
      current_data = {
        token_id: self._sanitize_attachment(item) if isinstance(item, dict) else item
        for token_id, item in current_data.items()
      }

    new_attachments = {}

    for _position, token in enumerate(order):
      kind, token_id = token.split(":", 1)

      # ===========================
      # 1) EXISTING ATTACHMENT
      # ===========================
      if kind == "attachment":
        if token_id in delete_ids:
          continue

        # keep existing
        if token_id in current_data:
          new_attachments[token_id] = current_data[token_id]

          # tambahkan/overwrite colSize
          if token_id in colsize_map:
            new_attachments[token_id]["colSize"] = colsize_map[token_id]
          if token_id in remark_map:
            new_attachments[token_id]["remark"] = remark_map[token_id]
          if token_id in description_map:
            new_attachments[token_id]["description"] = description_map[token_id]
          if token_id in maxheight_map:
            new_attachments[token_id]["maxHeight"] = maxheight_map[token_id]

        continue

      # ===========================
      # 2) NEW FILE
      # ===========================
      if kind == "new":
        if token_id not in new_files:
          continue

        info = new_files[token_id]

        uploaded = storage.upload_file(
          file_path=f"{base_path}-{token_id}",
          data=info["file"],
          content_type=info["content_type"],
        )

        new_attachments[token_id] = {
          "path": uploaded["path"],
          "storage": uploaded["id"],
          "colSize": colsize_map.get(token_id, None),
          "remark": remark_map.get(token_id, None),
          "description": description_map.get(token_id, None),
          "maxHeight": maxheight_map.get(token_id, None),
        }

    # update DB
    obj = self.db.execute(select(self.model).where(self.model.id == req_id)).scalars().first()

    self.db.execute(update(self.model).where(self.model.id == req_id).values({column_attr: new_attachments}))
    self.db.commit()

    self.db.flush()
    self.db.refresh(obj)
    return obj

  def _sanitize_attachment(self, attachment: dict) -> dict:
    allowed_keys = [
      "path",
      "storage",
      "colSize",
      "remark",
      "description",
      "maxHeight",
    ]
    return {key: attachment[key] for key in allowed_keys if key in attachment}

  def _resolve_column(self, column: str) -> InstrumentedAttribute:
    if not hasattr(self.model, column):
      raise ValueError(f"Model {self.model.__name__} has no column '{column}'")
    return getattr(self.model, column)
