from typing import Any, Literal

from fastapi.encoders import jsonable_encoder
from sqlalchemy import Select, func, insert, select, update
from sqlalchemy.orm import Mapped, Session
from utils.audit_trail import define_datalog, extract_name, logs
from utils.responses import BadRequest400, NotFound404

from .query_builder.query_having import query_all as query_all_having
from .query_builder.query_helper import apply_pivot, get_column

# from .queries import BrowseSchema
from .query_builder.query_model import BrowseSchema
from .query_builder.query_where import query_all as query_all_where

from sqlalchemy import inspect
from db.database import engine


class StdRepo:
  def __init__(self, db: Session, model: Any) -> None:
    self.db = db
    self.model = model


  # ==================================================================
  # CREATE, UPDATE, BULK UPSERT
  # ==================================================================
  def create(self, values: dict):
    """Create one row to db. Return dict"""
    data = self.db.execute(insert(self.model).values(values).returning(self.model)).scalars().first()
    self.db.flush()
    self.db.refresh(data)
    if data is None:
      raise BadRequest400("Failed to save data")
    return jsonable_encoder(data)

  def update(self, values: dict, data: Any):
    """Create one row to db by id. Return dict."""
    self.db.execute(update(self.model).where(self.model.id == data.id).values(values))
    self.db.flush()
    self.db.refresh(data)
    return jsonable_encoder(data)

  def bulk_store(self, values: list[dict], action: Literal['insert', 'update']):
    """Bulk update / insert by values. Return int len(values)"""
    try:
      if action == 'insert': self.db.execute(insert(self.model).values(values))
      elif action == 'update': self.db.bulk_update_mappings(self.model, values) # type: ignore
      return len(values)
    except Exception as e:
      raise BadRequest400(f'Failed to store data {str(e)}', e) from e


  # ==================================================================
  # GET DETAIL BY ID
  # ==================================================================
  def get_id(self, id: int | str):
    """Get data detail by id. Return tupple"""
    data = self.db.query(self.model).where(self.model.id == id, self.model.deleted_at.is_(None)).first()
    if data is None:
      raise NotFound404()
    return data

  # ==================================================================
  # SOFT DELETE & RESTORE
  # ==================================================================
  def soft_delete(self, ids: list[str | int | None], cred: dict | None, action: str = "delete") -> dict[str, Any]:
    """Soft delete and restore | With logs. Return {message: success, data: data_log}"""
    username = cred.get("username", "") if cred else ""
    stmt = None
    # 1. Get Data
    data_log = []
    try:
      items_raw = self.db.query(self.model).where(self.model.id.in_(ids)).all()
      for item in items_raw:
        item_dict = jsonable_encoder(item)
        row = define_datalog(name=extract_name(item_dict), before=item_dict)
        data_log.append(row)
    except Exception as e:
      raise BadRequest400(str(e), e)

    # 2. Execution
    try:
      values: dict = {}
      if action == "delete":
        values["deleted_at"] = func.now()
        if hasattr(self.model, "deleted_by"):
          values["deleted_by"] = username
      elif action == "restore":
        values["deleted_at"] = None
        if hasattr(self.model, "deleted_by"):
          values["deleted_by"] = None
      else:
        raise BadRequest400(f"Invalid type: {type}")

      stmt = update(self.model).where(self.model.id.in_(ids)).values(**values)
      self.db.execute(stmt)
    except Exception as e:
      raise BadRequest400(str(e), e)

    # 3. Save the logs
    try:
      logs(type=action, model=self.model, data=data_log, cred=cred)
    except Exception as e:
      print("Failed to execute logs: ", e)
    # db.commit()
    return {"message": "success", "data": data_log}

  # ==================================================================
  # GET INDEX BY QUERIES
  # ==================================================================
  # ---------- COUNT ---------- #
  def get_count(self, query: Select, db: Session) -> int:
    try:
      count_q = select(func.count()).select_from(query.subquery())
      return db.scalar(count_q) or 0
    except Exception as e:
      raise BadRequest400(f"Count error: {e}", e)

  # ---------- PAGINATION ---------- #
  def apply_pagination(self, query: Select, limit: int, page: int) -> Select:
    """Apply limit + offset"""
    try:
      if limit == 0: return query
      offset = limit * (page - 1)
      return query.limit(limit).offset(offset)
    except Exception as e:
      raise BadRequest400(f"Pagination error: {str(e)}", e)

  # ---------- LIST (NO PAGINATION) ---------- #
  def apply_limit(self, query: Select, limit: int) -> Select:
    """Apply limit only"""
    try:
      if limit > 0: return query.limit(limit)
      return query
    except Exception as e:
      raise BadRequest400(f"Limit error: {str(e)}", e)

  # ---------- GROUP SELECT | AUTOCOMPLETE ---------- #
  def apply_group_select(self, model: dict[str, Mapped], query: Select, group_select: str, limit: int):
    """Apply Group Select"""
    try:
      group_col = get_column(model, group_select)
      query = query.add_columns(group_col).where(group_col.isnot(None)).group_by(group_col)
      query = self.apply_limit(query, limit)
      result = self.db.execute(query).scalars().all()
      return result
    except Exception as e:
      raise BadRequest400(f"Group Select error: {str(e)}", e)

  # ---------- BROWSE ---------- #
  def browse(self, browse_queries: BrowseSchema, model: dict[str, Mapped], query: Select | None = None, is_having: bool = False):
    """Core browse executor"""

    # Apply filter functions
    query = query_all_having(browse_queries=browse_queries, model=model, query=query) if is_having else query_all_where(browse_queries=browse_queries, model=model, query=query)

    # GROUPING MODE
    if browse_queries.group_select:
      return self.apply_group_select(model=model, query=query, group_select=browse_queries.group_select, limit=browse_queries.limit)

    # NORMAL MODE: add labeled columns and get rows
    for key, col in model.items():
      query = query.add_columns(col.label(key))
    paginated = self.apply_pagination(query, browse_queries.limit, browse_queries.page)
    rows = self.db.execute(paginated).all()
    items = [row._asdict() for row in rows]

    # PIVOT MODE
    if browse_queries.pivot:
      total = self.get_count(query, self.db) if browse_queries.table else 0
      pivot = apply_pivot(items, browse_queries.pivot)
      return {
        "total": total,
        "pivot": pivot,
        "items": items
      }

    # TABLE MODE (return total + items)
    if browse_queries.table:
      total = self.get_count(query, self.db)
      return {
        "total": total,
        "items": [row._asdict() for row in rows]
      }

    # NON-TABLE MODE
    return items

  # ==================================================================
  # CODE GENERATOR
  # ==================================================================
  def get_last_serial_code_by_pattern(self, model: Any, field_name: str, search_pattern: str) -> str | None:
    """
    Queries the database for the most recent code matching the ILIKI pattern.
    """
    column = getattr(model, field_name)
    stmt = select(column).where(column.ilike(search_pattern)).order_by(func.length(column).desc(), column.desc()).limit(1)
    return self.db.execute(stmt).scalar_one_or_none()

  def get_last_codes_for_prefixes(self, model: Any, prefixes: list[str], field_name: str) -> dict[str, str | None]:
    """
    Returns a dictionary mapping each prefix to its latest existing code.
    Example return: {"CH-251223-": "CH-251223-0042", "CH-251224-": None}
    """
    column = getattr(model, field_name)
    if not prefixes:
      return {}

    results = {}
    for prefix in prefixes:
      search_pattern = f"{prefix}%"
      stmt = select(column).where(column.ilike(search_pattern)).order_by(func.length(column).desc(), column.desc()).limit(1)
      results[prefix] = self.db.execute(stmt).scalar_one_or_none()

    return results
  
  def get_columns_from_schema_tables(
      self,
      schema_tables: list[str],
      filter_types: list[str] | None = None,
      columns_custom: list[str] = []
  ) -> list[str]:

      inspector = inspect(engine)

      results = columns_custom or []

      for item in schema_tables:
          try:
            schema, table = item.split(".")

            columns = inspector.get_columns(table, schema=schema)

            for col in columns:
                col_name = col["name"]
                col_type = col["type"].__class__.__name__.upper()
                print(col_type)

                # flexible filter
                if filter_types and not any(ft in col_type for ft in filter_types):
                    continue

                results.append(f"{schema}.{table}.{col_name}")

          except ValueError:
              print(f"Invalid format: {item}, expected 'schema.table'")
          
          except Exception as e:
             print(f"Invalid format: {item}, expected 'schema.table'")


      return results

