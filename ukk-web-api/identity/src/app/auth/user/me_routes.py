from typing import Annotated

from app.auth.oauth2 import get_cred
from db.database import get_db
from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session
from utils.repo.queries import BrowseSchema, browse_query
from utils.responses import BadRequest400, NotFound404, res_success

from .models import User as BaseModel
from .schema import ChangePass, FavMenu, UserBase
from .service.get import get_by_cred, get_cred_fav_menu, get_cred_notif
from .service.store import post_pict, update_by_cred, update_password, update_sign

path = 'me'
router = APIRouter(prefix=f'/v1/{path}', tags=[path], dependencies=[])
module_permission = False

########### ME ###########
@router.get("")
def user_profile(
    db: Annotated[Session, Depends(get_db)],
    cred: Annotated[dict, Depends(get_cred)],
    refresh_token: int | None = 0,
):
    data = get_by_cred(cred, db, refresh_token)
    return res_success(data=data)

@router.get("/notifications")
def me_notif(
    browse_queries: Annotated[BrowseSchema, Depends(browse_query)],
    db: Annotated[Session, Depends(get_db)],
    cred: Annotated[dict, Depends(get_cred)],
    clear: bool = False,
):
    data = get_cred_notif(browse_queries, db, cred, clear)
    return res_success(data=data)

@router.post("/favmenu")
def me_fav_menu(
        request: FavMenu,
        db: Annotated[Session, Depends(get_db)],
        cred: Annotated[dict, Depends(get_cred)],
    ):
    data = get_cred_fav_menu(request, db, cred)
    return res_success(data=data)

@router.put("/update")
def me_update(
        request: UserBase,
        db: Annotated[Session, Depends(get_db)],
        cred: Annotated[dict, Depends(get_cred)],
    ):
    data = update_by_cred(request, db, cred)
    return res_success(data=data, db=db)

@router.put("/change-password")
def me_password(
        request: ChangePass,
        db: Annotated[Session, Depends(get_db)],
        cred: Annotated[dict, Depends(get_cred)],
    ):
    data = update_password(request, db, cred)
    return res_success(data=data, db=db)

@router.post("/change-picture")
async def change_picture(
    db: Annotated[Session, Depends(get_db)],
    cred: Annotated[dict, Depends(get_cred)],
    file: UploadFile = File(...)
):
    contents = await file.read()
    content_type = file.content_type if file.content_type else 'image/png'
    filesize = len(contents)
    max_size = 10 * 1024 * 1024
    if filesize > max_size:
        raise BadRequest400(f"Max filesize: {10} Mb!")
    data = db.query(BaseModel.id).filter(BaseModel.username == cred['username']).first()
    if data is None:
        raise NotFound404('invalid credential')
    user_id = data.id
    data = post_pict(id=user_id, db=db, cred=cred, file=contents, content_type=content_type)
    return res_success(data=data, db=db)

@router.post("/change-sign")
async def change_sign(
    db: Annotated[Session, Depends(get_db)],
    cred: Annotated[dict, Depends(get_cred)],
    sign_file: UploadFile | None = File(None),
    sign_with_stamp_file: UploadFile | None = File(None)
):
    sign_contents = None
    sign_type = ''
    if sign_file:
        sign_contents = await sign_file.read()
        filesize = len(sign_contents)
        max_size = 3 * 1024 * 1024
        if filesize > max_size: raise BadRequest400("Max filesize: 3 Mb!")
        if sign_file.content_type: sign_type = sign_file.content_type

    sign_with_stamp_contents = None
    sign_with_stamp_type = ''
    if sign_with_stamp_file:
        sign_with_stamp_contents = await sign_with_stamp_file.read()
        filesize = len(sign_with_stamp_contents)
        max_size = 3 * 1024 * 1024
        if filesize > max_size: raise BadRequest400("Max filesize: 3 Mb!")
        if sign_with_stamp_file.content_type: sign_with_stamp_type = sign_with_stamp_file.content_type

    files = {
        "sign": {
            "file": sign_contents,
            "type": sign_type
        },
        "sign_with_stamp": {
            "file": sign_with_stamp_contents,
            "type": sign_with_stamp_type
        }
    }
    data = db.query(BaseModel.id).filter(BaseModel.username == cred['username']).first()
    if data is None:
        raise NotFound404('invalid credential')

    user_id = data.id
    data = update_sign(id=user_id, db=db, cred=cred, files=files)
    return res_success(data=data, db=db)
