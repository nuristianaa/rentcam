import datetime
from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.orm import Session
from utils.audit_trail import define_datalog, logs
from utils.repo.queries import BrowseSchema
from utils.responses import BadRequest400
from utils.std_service import StdService

from app.master.item_categories.models import ItemCategory
from app.transaction.rentals.repo import RentalRepo

from .models import Item as Model
from .models import Req, tbl_select
from .repo import ItemRepo

VALID_CONDITIONS = ['baik', 'rusak_ringan']


class ItemService(StdService):
  def __init__(self, db: Session, cred: dict | None) -> None:
    self.repo = ItemRepo(db=db)
    super().__init__(db, cred, self.repo)

  def _validate_category(self, category_id: int | None):
    """Pastikan category_id ada dan tidak terhapus."""
    if not category_id:
      return
    cat = self.db.query(ItemCategory).filter(
      ItemCategory.id == category_id,
      ItemCategory.deleted_at.is_(None)
    ).first()
    if not cat:
      raise BadRequest400(f"Kategori dengan ID {category_id} tidak ditemukan.")

  def store(self, req: Req, id: int | None = None):
    # 1. Getting data first
    if id:
      data = self.repo.get_id(id=id)
      before = jsonable_encoder(data)

    values = req.model_dump(exclude_unset=True)

    # 2. Validasi
    if self.repo.get_by_code(req.code, exclude_id=id):
      raise BadRequest400(f"Kode alat '{req.code}' sudah digunakan.")

    self._validate_category(req.category_id)

    if req.condition and req.condition not in VALID_CONDITIONS:
      raise BadRequest400(f"Kondisi tidak valid. Pilihan: {', '.join(VALID_CONDITIONS)}")

    stock_total     = req.stock_total or 0
    stock_available = req.stock_available or 0
    if stock_available > stock_total:
      raise BadRequest400("Stock tersedia tidak boleh melebihi stock total.")

    # 3. Execute
    try:
      if id:
        log_type = 'update'
        values['updated_by'] = self.username
        data = self.repo.update(values=values, data=data)
        log_name = f"{data.get('code')} - {data.get('name')}"
        data_log = define_datalog(name=log_name, before=before, after=data)
      else:
        log_type = 'create'
        values['created_by'] = self.username
        data = self.repo.create(values=values)
        log_name = f"{data.get('code')} - {data.get('name')}"
        data_log = define_datalog(name=log_name, after=data)

      logs(type=log_type, model=Model, cred=self.cred, data=data_log, schema='master')
      return data
    except BadRequest400:
      raise
    except Exception as e:
      raise BadRequest400(str(e), e)

  def get_availability(self, id: int, start_date: datetime.date, end_date: datetime.date):
    try:
      item = self.repo.get_id(id=id)
      rental_repo = RentalRepo(db=self.db)
      reservations = rental_repo.get_reserved_quantities_by_item(id, start_date, end_date)

      days: list[dict[str, int | str | bool]] = []
      current = start_date
      while current <= end_date:
        reserved = 0
        for rental_start, rental_end, qty in reservations:
          if rental_start <= current <= rental_end:
            reserved += qty
        available_quantity = max((item.stock_total or 0) - reserved, 0)
        days.append({
          'date': current.isoformat(),
          'reserved_quantity': reserved,
          'available_quantity': available_quantity,
          'available': available_quantity > 0,
        })
        current += datetime.timedelta(days=1)

      next_available_date = next((day['date'] for day in days if day['available']), None)

      return {
        'item_id': item.id,
        'item_name': item.name,
        'stock_total': item.stock_total or 0,
        'stock_available': item.stock_available or 0,
        'start_date': start_date.isoformat(),
        'end_date': end_date.isoformat(),
        'days': days,
        'next_available_date': next_available_date,
      }
    except BadRequest400:
      raise
    except Exception as e:
      raise BadRequest400(str(e), e)

  def get_index(self, browse_queries: BrowseSchema):
    try:
      query = select(Model).join(
        ItemCategory,
        ItemCategory.id == Model.category_id,
        isouter=True
      )
      model = tbl_select(custom_col={"category_name": ItemCategory.name})
      return self.repo.browse(browse_queries=browse_queries, model=model, query=query)
    except Exception as e:
      raise BadRequest400(str(e), e) from e

  def get_id(self, id: int):
    try:
      return self.repo.get_id(id=id)
    except Exception as e:
      raise BadRequest400(str(e), e)