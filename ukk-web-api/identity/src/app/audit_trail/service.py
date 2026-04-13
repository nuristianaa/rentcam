# from utils.helpers.date import today, currentmillis
from datetime import datetime as dt_datetime
from itertools import groupby

from sqlalchemy import and_, func, select, tuple_
from sqlalchemy.orm import Session, aliased
from utils.helpers.approvers import get_approvers
from utils.repo.queries import BrowseSchema, browse
from utils.responses import BadRequest400

from .models import AuditTrail as Model
from .models import GeneratePdfReq, OtherBrowseReq, tbl_select, tbl_select_with_data

# UNUSED | FOUND A BETTER WAY
# LAST_DT = currentmillis()
# LISTS: list[Req] = []

# def create(req: list[Req], db: Session, cred: dict | None):
#   global LAST_DT, LISTS
#   LISTS += req
#   sequence = 10 # in seconds
#   now = currentmillis()
#   if now - LAST_DT > (sequence * 1000):
#     try:
#       if len(LISTS) > 0:
#         values = [v.model_dump() for v in LISTS]
#         db.execute( insert(Model).values(values) )
#         db.commit()
#         LISTS = []
#       return 'success'
#     except Exception as e:
#       return 'failed' + str(e)
#   return 'save to lists'


def get_index(browse_queries: BrowseSchema, db: Session, date_from: str, date_to: str, other_queries: OtherBrowseReq):
  """Returns list based on query."""
  try:
    if other_queries.fetch_column and other_queries.app:
      return _get_modules_by_app(other_queries.app, db)
    elif other_queries.fetch_module:
      return _get_modules(db=db, date_from=date_from, date_to=date_to)
    else:
      query = select()
      query = query.where(Model.created_at >= date_from, Model.created_at <= date_to)
      columns = tbl_select
      if other_queries.with_data:
        columns = tbl_select_with_data

      if other_queries.app:
        query = query.where(Model.app == other_queries.app)

      if other_queries.module:
        app, schema, module = (
          other_queries.module.split(".", 2) if "." in other_queries.module else (None, None, other_queries.module)
        )
        query = query.where(Model.app == app, Model.schema == schema, Model.module == module)
        columns = tbl_select_with_data

      data = browse(browse_queries=browse_queries, model=columns, query=query, db=db)
      return data
  except Exception as e:
    msg = "Audit Trail get_index: " + str(e)
    raise BadRequest400(msg, e)


def get_detail(db: Session, id: str):
  data = db.query(Model.data).filter(Model.id == id).scalar()
  return data


def generate_pdf(req: GeneratePdfReq, db: Session, cred: dict):
  try:
    if not req.configs:
      return {}

    values: dict = req.model_dump(exclude_unset=True)
    approvers = get_approvers(approval_meta=values, token=cred["token"], with_text=False)

    result = []

    filter_tuples = [tuple(c.module.split(".", 2)) for c in req.configs if c.module and "." in c.module]

    previous_data_col = (
      func.lag(Model.data)
      .over(partition_by=(Model.app, Model.schema, Model.module, Model.module_id), order_by=Model.created_at)
      .label("previous_data")
    )

    cte_subquery = (
      select(Model, previous_data_col)
      .where(tuple_(Model.app, Model.schema, Model.module).in_(filter_tuples))
      .cte("lagged_logs")
    )

    cte_aliased = aliased(cte_subquery)

    query = (
      select(cte_aliased)
      .where(cte_aliased.c.created_at >= req.date_from, cte_aliased.c.created_at <= req.date_to)
      .order_by(cte_aliased.c.app, cte_aliased.c.schema, cte_aliased.c.module)
    )

    log_rows = db.execute(query).all()

    config_columns_map = {c.module: set(c.columns or []) for c in req.configs if c.module and c.columns}

    for log_row in log_rows:
      ref_name = log_row.name
      module_key = f"{log_row.app}.{log_row.schema}.{log_row.module}"
      columns = config_columns_map.get(module_key, set())

      current_data = log_row.data or {}

      # previous_data = log_row.previous_data
      previous_data = current_data.get("_before", log_row.previous_data)

      if not log_row.data:
        continue

      for key, value in log_row.data.items():
        if key == "_before":
          continue

        if isinstance(value, list):
          prev_list = []
          if previous_data and isinstance(previous_data.get(key), list):
            prev_list = previous_data[key]

          for val in value:
            for k, v in val.items():
              if k in columns:
                prev_val_dict = None
                if "id" in val and prev_list:
                  prev_val_dict = next((item for item in prev_list if item.get("id") == val["id"]), None)

                prev_v = prev_val_dict.get(k) if prev_val_dict else None
                result.append(_build_result_row(log_row, ref_name, k, v, prev_v))
        else:
          if key in columns:
            prev_value = previous_data.get(key) if previous_data else None
            result.append(_build_result_row(log_row, ref_name, key, value, prev_value))

    type_order = {"create": 0, "update": 1, "delete": 2}
    result.sort(
      key=lambda x: (
        x["app"],
        x["module"],
        type_order.get(x["type"], 99),
        x["ref"],
        x["date"],
      )
    )

    grouped_result = []
    group_key_func = lambda x: (x["app"], x["module"]) # noqa E731

    for (app, module), group in groupby(result, key=group_key_func):
      grouped_result.append({"app": app, "module": module, "data": list(group)})

    return {"data": grouped_result, "approvers": approvers}
  except Exception as e:
    msg = "Audit Trail generate_pdf: " + str(e)
    raise BadRequest400(msg, e)


def _get_modules_by_app(app: str, db: Session) -> dict[str, list[str]]:
  modules = db.query(Model.schema, Model.module).filter(Model.app == app).distinct().all()

  module_keys: dict[str, list[str]] = {}

  for (
    schema,
    module,
  ) in modules:
    # Get the first record for the module
    first_record = db.query(Model).filter(Model.app == app, Model.module == module).order_by(Model.id.asc()).first()
    if first_record and isinstance(first_record.data, dict):
      if first_record.data.get("data") and isinstance(first_record.data["data"], list):
        module_keys[f"{app}.{schema}.{module}"] = list(first_record.data["data"][0].keys())
      else:
        module_keys[f"{app}.{schema}.{module}"] = list(first_record.data.keys())
    else:
      module_keys[module] = []

  return module_keys


def _get_modules(db: Session, date_from: str, date_to: str) -> dict[str, list[str]]:
  modules = (
    db.query(Model.app, Model.schema, Model.module)
    .where(Model.created_at >= date_from, Model.created_at <= date_to)
    .distinct()
    .all()
  )

  if not modules:
    return {}

  module_tuples = [(m.app, m.schema, m.module) for m in modules]

  subq = (
    db.query(Model.app, Model.schema, Model.module, func.min(Model.created_at).label("first_created_at"))
    .filter(tuple_(Model.app, Model.schema, Model.module).in_(module_tuples))
    .group_by(Model.app, Model.schema, Model.module)
    .subquery()
  )

  first_records = (
    db.query(Model)
    .join(
      subq,
      and_(
        Model.app == subq.c.app,
        Model.schema == subq.c.schema,
        Model.module == subq.c.module,
        Model.created_at == subq.c.first_created_at,
      ),
    )
    .all()
  )

  module_keys: dict[str, list[str]] = {}
  for record in first_records:
    key = f"{record.app}.{record.schema}.{record.module}"
    data = record.data
    if isinstance(data, dict):
      if data.get("data") and isinstance(data["data"], list) and data["data"]:
        module_keys[key] = list(data["data"][0].keys())
      else:
        module_keys[key] = list(data.keys())
    else:
      module_keys[key] = []

  return module_keys


def _build_result_row(log_row, ref_name, column, value, prev_value):
  """
  Helper to build a single result dictionary.
  Accepts a 'log_row' (SQLAlchemy Row) and a 'prev_value'.
  """
  created_at_val = log_row.created_at
  return {
    "app": log_row.app,
    "module": log_row.module,
    "ref": ref_name,
    "column": column,
    "type": log_row.type,
    "prev_value": prev_value,
    "after_value": value,
    "user": log_row.username,
    "date": created_at_val.strftime("%Y-%m-%d %H:%M:%S") if isinstance(created_at_val, dt_datetime) else created_at_val,
  }
