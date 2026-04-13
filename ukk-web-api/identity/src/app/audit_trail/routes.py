from datetime import datetime
from typing import Annotated

from app.auth.oauth2 import check_permission, get_cred
from db.database import get_db, get_db_log
from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from starlette.templating import _TemplateResponse
from ui.index import render
from utils.helpers.date import format_date, now
from utils.repo.queries import BrowseSchema, browse_query
from utils.responses import res_success

from .models import GeneratePdfReq, OtherBrowseReq, Req, other_browse_query
from .service import generate_pdf, get_detail, get_index
from .service_background import AUDIT_QUEUE

path = "audit-trails"
router = APIRouter(prefix=f"/v1/{path}", tags=[path], dependencies=[])


def get_ui_path(type: str) -> str:
  return f"app/audit_trail/templates/{type}.html"


# BROWSE
@router.get("")
def browse(
  cred: Annotated[dict, Depends(get_cred)],
  db_main: Annotated[Session, Depends(get_db)],
  db: Annotated[Session, Depends(get_db_log)],
  browse_queries: Annotated[BrowseSchema, Depends(browse_query)],
  other_queries: Annotated[OtherBrowseReq, Depends(other_browse_query)],
  date_from: str | None = None,
  date_to: str | None = None,
):
  check_permission(cred=cred, db=db_main, module=f"{path}-browse")
  current_year = datetime.now().year
  if date_from is None:
    date_from = f"{current_year}-01-01"
  if date_to is None:
    date_to = f"{current_year + 1}-01-01"
  data = get_index(
    browse_queries=browse_queries, db=db, date_from=date_from, date_to=date_to, other_queries=other_queries
  )
  return res_success(data=data)


@router.get("/{id}")
def browse_id(
  id: str,
  db_main: Annotated[Session, Depends(get_db)],
  db: Annotated[Session, Depends(get_db_log)],
  cred: Annotated[dict, Depends(get_cred)],
):
  check_permission(cred=cred, db=db_main, module=f"{path}-read")
  data = get_detail(db, id)
  return res_success(data=data)


@router.post("")
def post_create(req: list[Req], cred: Annotated[dict, Depends(get_cred)]):
  for r in req:
    AUDIT_QUEUE.put(r.model_dump(by_alias=True))
  return {"message": "audit trails enqueued"}


@router.post("/generate-pdf")
def generate(
  request: Request,
  req: GeneratePdfReq,
  db_main: Annotated[Session, Depends(get_db)],
  db: Annotated[Session, Depends(get_db_log)],
  cred: Annotated[dict, Depends(get_cred)],
) -> _TemplateResponse:
  check_permission(cred=cred, db=db_main, module=f"{path}-read")
  ui_path = get_ui_path("generate_pdf")
  data = generate_pdf(req, db=db, cred=cred)

  date_range = ""
  if req.date_from and req.date_to:
    date_from = format_date(req.date_from, format_to="%m/%d/%Y", format_fr="%Y-%m-%d")
    date_to = format_date(req.date_to, format_to="%m/%d/%Y", format_fr="%Y-%m-%d")
    date_range = f"{date_from} - {date_to}"

  modules = ""
  if req.configs:
    modules = ", ".join(
      f"{c.module.split('.')[0]} - {c.module.split('.')[2].capitalize()}" for c in req.configs if c.module
    )

  params = {
    "title": "Audit Trail PDF",
    "data": data["data"],
    "approvers": data["approvers"],
    "date_range": date_range,
    "req_modules": modules,
    "company_code": req.company_code,
    "printed_by": cred["username"],
    "printed_at": now(format="%m/%d/%Y %H:%M:%S"),
  }
  return render(
    path=ui_path,
    request=request,  # No request needed for PDF generation
    params=params,
  )


# CREATE | UNUSED -> FOUND A BETTER WAY
# @router.post('')
# def post_create(
#     req: list[Req],
#     bt: BackgroundTasks,
#     db: Annotated[Session, Depends(get_db_log)],
#     cred: Annotated[dict, Depends(get_cred)],
# ):
#     bt.add_task(create, req, db, cred)
#     data = {'message': 'audit trails triggered in background'}
#     return res_success(data=data)
