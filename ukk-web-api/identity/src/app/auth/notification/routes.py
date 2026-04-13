from typing import Annotated

from app.auth.oauth2 import get_cred
from db.database import get_db
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from utils.responses import res_success

from .models import SubscribeReq
from .service import get_id, store_subscriber

path = "auth/notifications"
router = APIRouter(prefix=f"/v1/{path}", tags=[path], dependencies=[])

@router.get("/{id}")
def browse_id(
  id: int|str,
  db: Annotated[Session, Depends(get_db)],
  cred: Annotated[dict, Depends(get_cred)],
):
  data = get_id(id, db)
  return res_success(data=data)


# @router.post("")
# def post_create(req: SendReqNotif, cred: Annotated[dict, Depends(get_cred)]):# -> dict[str, Any]:
#   send_notif(req)
#   data = {'message': 'Notif triggered in background'}
#   return res_success(data=data)


@router.post("/subscribe")
def subscribe(req: SubscribeReq, db: Annotated[Session, Depends(get_db)], cred: Annotated[dict, Depends(get_cred)]):
  data = store_subscriber(req=req, db=db)
  return res_success(data=data)
