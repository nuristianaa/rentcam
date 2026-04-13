
from typing import Any

from sqlalchemy import bindparam, delete, insert, select, text, tuple_, update
from sqlalchemy.orm import Session
from utils.repo.queries import BrowseSchema
from utils.repo.std_repo import StdRepo
from utils.responses import BadRequest400

from .models import Req
from .models import ItemCategory as Model


class ItemCategoryRepo(StdRepo):
  def __init__(self, db: Session):
    super().__init__(db, Model)
