from datetime import datetime

from db.database import Base
from pydantic import BaseModel
from sqlalchemy import func, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql.sqltypes import BigInteger, Boolean, DateTime, String, Text


class Notification(Base):
  __tablename__ = "notifications"
  __table_args__ = {"schema": "auth", "extend_existing": True}

  id: Mapped[int|str] = mapped_column(BigInteger, primary_key=True)
  username: Mapped[str] = mapped_column(String, nullable=True)
  user_id: Mapped[int|None] = mapped_column(nullable=True)
  is_read: Mapped[bool] = mapped_column(Boolean, default=False)
  app: Mapped[str|None] = mapped_column(String, nullable=True)
  title: Mapped[str|None] = mapped_column(String, nullable=True)
  description: Mapped[str|None] = mapped_column(Text, nullable=True)
  path: Mapped[str|None] = mapped_column(String, nullable=True)
  type: Mapped[str|None] = mapped_column(String, nullable=True)
  color: Mapped[str|None] = mapped_column(String, nullable=True)
  icon: Mapped[str|None] = mapped_column(String, nullable=True)

  created_by: Mapped[str|None] = mapped_column(String, nullable=True)
  updated_by: Mapped[str|None] = mapped_column(String, nullable=True)
  deleted_by: Mapped[str|None] = mapped_column(String, nullable=True)
  created_at: Mapped[datetime|None] = mapped_column(DateTime, default=func.now())
  updated_at: Mapped[datetime|None] = mapped_column(DateTime, default=func.now(), onupdate=func.now())
  deleted_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)

class PushSubscription(Base):
  __tablename__ = "notif_push_subs"
  __table_args__ = {"schema": "auth", "extend_existing": True}

  id: Mapped[int|str] = mapped_column(UUID, primary_key=True, server_default=text("gen_random_uuid()"))
  user_id: Mapped[int] = mapped_column(BigInteger, nullable=True)
  username: Mapped[str] = mapped_column(String, nullable=True)
  endpoint: Mapped[str] = mapped_column(String, unique=True)
  p256dh: Mapped[str] = mapped_column(String, unique=True)
  auth: Mapped[str] = mapped_column(String, unique=True)
  created_at: Mapped[datetime|None] = mapped_column(DateTime, default=func.now())


tbl_select = {
  'id': Notification.id,
  'username': Notification.username,
  'is_read': Notification.is_read,
  'app': Notification.app,
  'title': Notification.title,
  'description': Notification.description,
  'path': Notification.path,
  'type': Notification.type,
  'color': Notification.color,
  'icon': Notification.icon,
  'created_by': Notification.created_by,
  'created_at': Notification.created_at,
  'updated_by': Notification.updated_by,
  'updated_at': Notification.updated_at,
  'deleted_by': Notification.deleted_by,
  'deleted_at': Notification.deleted_at
}


class Req(BaseModel):
  usernames: list[str] | None = None
  user_id    : int|None = None
  app: str | None = None
  title: str | None = None
  description: str | None = None
  path: str | None = None
  type: str | None = None
  channels: list[str] | None = None

class SubscriberKeys(BaseModel):
  p256dh: str|int|None = None
  auth: str|int|None = None

class SubscribeBody(BaseModel):
  endpoint: str|None = None
  keys: SubscriberKeys|None = None

class SubscribeReq(BaseModel):
  username: str|None = None
  user_id: int|None = None
  device_id: str|None = None
  subscription: SubscribeBody|None = None
