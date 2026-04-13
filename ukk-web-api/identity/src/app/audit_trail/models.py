from datetime import datetime
from typing import Any

from db.database import Base
from pydantic import BaseModel, Field
from sqlalchemy import func, text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql.sqltypes import DateTime, String


class AuditTrail(Base):
  __tablename__ = "audit_trails"
  # __table_args__ = {"extend_existing": True}
  __table_args__ = {"schema": "public"}

  id: Mapped[int | str] = mapped_column(UUID, primary_key=True, index=True, server_default=text("gen_random_uuid()"))
  type: Mapped[str | None] = mapped_column(String, nullable=True)
  app: Mapped[str | None] = mapped_column(String, nullable=True)
  schema: Mapped[str | None] = mapped_column(String, nullable=True)
  module: Mapped[str | None] = mapped_column(String, nullable=True)
  module_id: Mapped[str | None] = mapped_column(String, nullable=True)
  name: Mapped[str | None] = mapped_column(String, nullable=True)
  username: Mapped[str | None] = mapped_column(String, nullable=True)
  data: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
  created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())


tbl_select: dict[str, Mapped] = {
  "id": AuditTrail.id,
  "type": AuditTrail.type,
  "app": AuditTrail.app,
  "schema": AuditTrail.schema,
  "module": AuditTrail.module,
  "module_id": AuditTrail.module_id,
  "name": AuditTrail.name,
  "username": AuditTrail.username,
  "created_at": AuditTrail.created_at,
}

tbl_select_with_data: dict[str, Mapped] = {
  "id": AuditTrail.id,
  "type": AuditTrail.type,
  "app": AuditTrail.app,
  "schema": AuditTrail.schema,
  "module": AuditTrail.module,
  "module_id": AuditTrail.module_id,
  "name": AuditTrail.name,
  "username": AuditTrail.username,
  "data": AuditTrail.data,
  "created_at": AuditTrail.created_at,
}


# Pydantic
class Req(BaseModel):
  type: str | None = None
  app: str | None = None
  schema_name: str = Field(alias="schema")

  class Config:
    populate_by_name = True

  module: str | None = None
  module_id: str | None = None
  name: str | None = None
  username: str | None = None
  data: Any | None = None


class GeneratePdfConfig(BaseModel):
  module: str | None = None
  columns: list[str] | None = None


class Approver(BaseModel):
  name: str | None = None
  id: str | int | None = None
  title: str | None = None
  sign_url: str | None = None
  sign_path: str | None = None


class BlockApprover(BaseModel):
  id: str | int | None = None
  data: Approver | None = None
  cols: int


class SignBlock(BaseModel):
  id: str | int
  cols: int
  title: str
  approvers: list[BlockApprover]
  children: list["SignBlock"]


class GeneratePdfReq(BaseModel):
  configs: list[GeneratePdfConfig] | None = None
  date_from: str | None = None
  date_to: str | None = None
  company_code: str | None = None
  sign_placements: list[SignBlock]


class OtherBrowseReq(BaseModel):
  with_data: bool = False
  app: str | None = None
  module: str | None = None
  fetch_module: bool | None = False
  fetch_column: bool | None = False


def other_browse_query(
  with_data: bool = False,
  app: str | None = None,
  module: str | None = None,
  fetch_module: bool | None = None,
  fetch_column: bool | None = None,
) -> OtherBrowseReq:
  return OtherBrowseReq(
    with_data=with_data,
    app=app,
    module=module,
    fetch_module=fetch_module,
    fetch_column=fetch_column,
  )
