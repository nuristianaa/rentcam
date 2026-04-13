from collections.abc import Mapping, Sequence
from typing import Any

from sqlalchemy import Column, ColumnElement, Select, func, update
from sqlalchemy.orm import Mapped, Session
from utils.responses import BadRequest400

from .query_builder.query_helper import get_column
from .query_builder.query_model import BrowseSchema, BulkId, browse_query
from .query_builder.query_where import query_all
from .services import logs

__all__ = ["browse_query", "BrowseSchema", "BulkId"]
summary_functions = {"sum": func.sum, "avg": func.avg, "min": func.min, "max": func.max, "count": func.count}

def get_count(query: Select[Any], db: Session) -> Any | None:
  """
  Return count of data
  """
  try:
    query = query.add_columns(func.count()).with_only_columns(func.count(), maintain_column_froms=True).order_by(None)
    return db.execute(query).scalars().one_or_none()
  except Exception as e:
    raise BadRequest400(str(e))


def get_summary(browse_queries: BrowseSchema, query: Select[Any], model: Mapping[str, Mapped | ColumnElement | Column], db: Session) -> dict[str, Any]:
  """
  Return summary of each column based on summary_map
  """
  try:
    if not browse_queries.summary or not browse_queries.summary_map:
      return {}

    select_exp = []
    labels = []

    for item in browse_queries.summary_map:
      parts = item.split(":")

      if len(parts) != 2:
        print(f"Skipping invalid summary_map item: {item}")
        continue

      col_name, fn_name = parts
      fn_name = fn_name.lower()

      if fn_name not in summary_functions:
        print(f"Skipping unsupported summary function: {fn_name}")
        continue

      column_obj = get_column(model=model, col=col_name)
      sql_func = summary_functions[fn_name]

      label = f"{col_name}_{fn_name}"
      labels.append(label)
      select_exp.append(sql_func(column_obj).label(label))

    if not select_exp:
      return {}

    summary_query = query.with_only_columns(*select_exp).order_by(None)

    result = db.execute(summary_query).first()

    if result:
      return result._asdict()
    else:
      return {label: None for label in labels}
  except Exception as e:
    raise BadRequest400(str(e))


def query_pagination(browse_queries: BrowseSchema, query: Select[Any]) -> Select[Any]:
  """
  Return list of data within pagination boundary
  """
  try:
    size = browse_queries.limit
    page = browse_queries.page
    ofs = size * (page - 1)
    query = query.limit(size).offset(ofs) if ofs > 0 else query.limit(size)

    return query
  except Exception as e:
    raise BadRequest400(str(e))


def query_list(browse_queries: BrowseSchema, query: Select[Any]) -> Select[Any]:
  """
  Return list of data within limit
  """
  try:
    size = browse_queries.limit
    if size != 0:
      query = query.limit(size)

    return query
  except Exception as e:
    raise BadRequest400(str(e))


def browse(
  *,
  browse_queries: BrowseSchema,
  model: Mapping[str, Mapped | ColumnElement | Column],
  query: Select[Any] | None = None,
  db: Session,
) -> Sequence[Any] | dict[str, Any] | list[dict[str, Any]]:
  """
  base function
  """
  # query params
  query = query_all(browse_queries=browse_queries, model=model, query=query)

  # query group
  if browse_queries.group_select:
    group_column = get_column(model, browse_queries.group_select)
    query = query.add_columns(group_column)
    query = query.where(group_column.isnot(None))
    query = query.group_by(group_column)
    query = query_list(browse_queries=browse_queries, query=query)
    # print(query)
    return db.execute(query).scalars().all()
  # add columns based on model params
  else:
    for key, value in model.items():
      query = query.add_columns(value.label(key))

  if browse_queries.table:
    total = get_count(query=query, db=db) or 0
    data = db.execute(query_pagination(browse_queries=browse_queries, query=query)).all()
    return {"total": total, "items": [row._asdict() for row in data]}

  if browse_queries.summary:
    summary = get_summary(browse_queries=browse_queries, query=query, model=model, db=db)
    return summary

  data = db.execute(query_list(browse_queries=browse_queries, query=query)).all()
  return [row._asdict() for row in data]


def soft_delete(
  request: BulkId,
  id: int | str | None,
  db: Session,
  model: Any,
  cred: dict | None,
  type: str = "delete",
  save_log: bool | None = True,
) -> dict[str, Any]:
  username = cred["username"] if cred else ""
  stmt = None
  if id:
    data = id
    try:
      if type == "delete":
        try:
          stmt = update(model).where(model.id == id).values(deleted_by=username, deleted_at=func.now())
        except Exception as _e:
          stmt = update(model).where(model.id == id).values(deleted_at=func.now())
      elif type == "restore":
        try:
          stmt = update(model).where(model.id == id).values(deleted_by=None, deleted_at=None)
        except Exception as _e:
          stmt = update(model).where(model.id == id).values(deleted_at=None)
      if stmt is not None:
        db.execute(stmt)
    except Exception as e:
      db.rollback()
      raise BadRequest400(str(e), e)
  elif request.id is not None and len(request.id) > 0:
    ids = request.id
    data = ids
    try:
      if type == "delete":
        try:
          stmt = update(model).where(model.id.in_(ids)).values(deleted_by=username, deleted_at=func.now())
        except Exception as _e:
          stmt = update(model).where(model.id.in_(ids)).values(deleted_at=func.now())
      elif type == "restore":
        try:
          stmt = update(model).where(model.id.in_(ids)).values(deleted_by=None, deleted_at=None)
        except Exception as _e:
          stmt = update(model).where(model.id.in_(ids)).values(deleted_by=None, deleted_at=None)
      if stmt is not None:
        db.execute(stmt)
    except Exception as e:
      db.rollback()
      raise BadRequest400(str(e), e)
  else:
    raise BadRequest400("No Data Delete")
  # Save the logs
  try:
    if save_log:
      logs(type=type, model=model, data=data, cred=cred, db=db)
  except Exception as e:
    print("repo queries soft_delete: ", e)
  # db.commit()
  return {"message": "success", "data": data}
