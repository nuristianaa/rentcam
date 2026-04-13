import json
import uuid
from typing import Annotated

from fastapi import Request
from fastapi.param_functions import Form
from pydantic import BaseModel
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession


class ReqFcm(BaseModel):
  fcm: str | None = None
  device_id: str | None = None
  platform: str | None = None
  username: str | None = None


class AzureToken(BaseModel):
  token: str | None = None
  access_token: str | None = None
  client_info: str | None = None
  id_token: str | None = None
  refresh_token: str | None = None

class ReqAuthAzure(BaseModel):
  oauth: AzureToken | None = None
  remember_me: bool | None = None
  is_mobile: bool | None = None
  device_id: str | None = None

class LoginForm:
  def __init__(
    self,
    *,
    username: Annotated[str,Form()],
    password: Annotated[str,Form()],
    remember_me: Annotated[bool,Form()] = False,
    is_mobile: Annotated[bool,Form()] = False,
    device_id: Annotated[str,Form()] = '',
  ):
    self.username = username
    self.password = password
    self.remember_me = remember_me
    self.is_mobile = is_mobile
    self.device_id = device_id

class ReqRefreshToken(BaseModel):
  refresh_token: str

def translate_uri(method: str, uri: str):
  isread = False
  isdelete = False
  lastword = uri.find('?')
  if (lastword > -1): uri = uri[:lastword]
  app = 'identity'
  apps = ['crm', 'engineering', 'finance', 'hris', 'procurement', 'project_management']
  for pref in apps:
    if uri.find(f'/{pref}/') == 0:
      app = pref
      uri = uri.replace(f'/{pref}/', '')

  uri = uri.replace('v1/', '')
  try:
    ursplit = uri.split('/')
    uri = ursplit[0] + '/' + ursplit[1]
    try:
      if method == 'GET': isread = bool(ursplit[2] is not None)
      elif method == 'DELETE': isdelete = bool(ursplit[2] == 'delete')
    except: ''
  except: ''
  action = 'browse'
  if method == 'GET': action = 'read' if isread else 'browse'
  elif method == 'POST': action = 'create'
  elif method == 'PUT': action = 'update'
  elif method == 'DELETE': action = 'delete' if isdelete else 'restore'

  return app, uri, action

def translate_uri2(uri: str):
  lastword = uri.find('?')
  if (lastword > -1):
    uri = uri[:lastword]
  app = 'identity'
  apps = ['crm', 'engineering', 'finance', 'hris', 'identity', 'procurement', 'project_management']
  for pref in apps:
    if uri.find(f'/{pref}/') == 0:
      app = pref
      uri = uri.replace(f'/{pref}/', '')
  uri = uri.replace('/v1/', '').replace('v1/', '')
  splt = uri.split("/")[:2]
  if len(splt) > 1:
    schema, module = splt[0], splt[1]
    uri = f'{schema}/{module}' if (check_type(module) == 'unknown') else schema
  else:
    uri = splt[0]
  return app, uri

def check_type(value: str):
  # Try integer first
  try:
    int(value)
    return "int"
  except ValueError:
    pass

  # Try UUID
  try:
    uuid.UUID(value)
    return "uuid"
  except (ValueError, TypeError):
    pass

  return "unknown"
