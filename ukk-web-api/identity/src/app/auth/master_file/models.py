from datetime import datetime
from enum import Enum
from typing import Annotated, Any

from db.database import Base
from fastapi import Form
from pydantic import BaseModel
from sqlalchemy import func
from sqlalchemy.orm import Mapped, column_property, mapped_column
from sqlalchemy.sql.sqltypes import BigInteger, Boolean, DateTime, String, Text


class MasterFile(Base):
  __tablename__ = "master_files"
  __table_args__ = {"schema": "auth"}

  id: Mapped[int]                  = mapped_column(BigInteger, primary_key=True, index=True)
  app: Mapped[str|None]            = mapped_column(String, nullable=True)
  name: Mapped[str|None]           = mapped_column(String, nullable=True)
  description: Mapped[str|None]    = mapped_column(Text, nullable=True)
  filename: Mapped[str|None]       = mapped_column(String, nullable=True)
  filetype: Mapped[str|None]       = mapped_column(String, nullable=True)
  path: Mapped[str|None]           = mapped_column(String, nullable=True)
  module: Mapped[str|None]         = mapped_column(String, nullable=True)
  reference_code: Mapped[str|None] = mapped_column(String, nullable=True)
  reference_id: Mapped[str|None]   = mapped_column(String, nullable=True)
  is_public: Mapped[bool|None]     = mapped_column(Boolean, nullable=True)
  storage_id: Mapped[str|None]     = mapped_column(String, nullable=True)
  base_url: Mapped[str|None]       = mapped_column(String, nullable=True)

  created_by: Mapped[str|None]     = mapped_column(String, nullable=True)
  updated_by: Mapped[str|None]     = mapped_column(String, nullable=True)
  deleted_by: Mapped[str|None]     = mapped_column(String, nullable=True)
  created_at: Mapped[datetime]     = mapped_column(DateTime, default=func.now())
  updated_at: Mapped[datetime]     = mapped_column(DateTime, default=func.now(), onupdate=func.now())
  deleted_at: Mapped[datetime|None]= mapped_column(DateTime, nullable=True)

class RequestCreate:
  def __init__(
    self,
    *,
    app: Annotated[str|None, Form()] = None,
    name: Annotated[str|None, Form()] = None,
    description: Annotated[str|None, Form()] = None,
    module: Annotated[str|None, Form()] = None,
    reference_code: Annotated[str|None, Form()] = None,
    reference_id: Annotated[str|int|None, Form()] = None,
    is_public: Annotated[bool|None, Form()] = False,
    delete_file: Annotated[str|int|None, Form()] = None,
  ):
    self.app = app
    self.name = name
    self.description = description
    self.module = module
    self.reference_code = reference_code
    self.reference_id = reference_id
    self.is_public = is_public
    self.delete_file = delete_file

# class RequestUpdate(RequestCreate):
#   id: Optional[int]

class Display(BaseModel):
  id: int | None
  app: str | None = None
  name: str | None = None
  description: str | None = None
  filename: str | None = None
  path: str | None = None
  module: str | None = None
  reference_code: str | None = None
  reference_id: str | None = None
  created_by: str | None      = None
  created_at: datetime | None = None
  updated_by: str | None      = None
  updated_at: datetime | None = None
  deleted_by: str | None      = None
  deleted_at: datetime | None = None

tbl_select: dict[str, Any] = {
  'id'            : MasterFile.id,
  'app'           : MasterFile.app,
  'name'          : MasterFile.name,
  'description'   : MasterFile.description,
  'filename'      : MasterFile.filename,
  'filetype'      : MasterFile.filetype,
  'path'          : MasterFile.path,
  'module'        : MasterFile.module,
  'reference_code': MasterFile.reference_code,
  'reference_id'  : MasterFile.reference_id,
  'is_public'     : MasterFile.is_public,
  'created_by'    : MasterFile.created_by,
  'updated_by'    : MasterFile.updated_by,
  'deleted_by'    : MasterFile.deleted_by,
  'created_at'    : MasterFile.created_at,
  'updated_at'    : MasterFile.updated_at,
  'deleted_at'    : MasterFile.deleted_at,
}

class ModeEnum(str, Enum):
  private = "private"
  public = "public"
