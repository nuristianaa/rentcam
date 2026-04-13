from sqlalchemy import not_, select
from utils.responses import BadRequest400

from .query_helper import (
  filter_list,
  get_column,
  parse_item,
  to_number,
)


# ===================
# Query Builder
# ===================
def query_where(b, model, q):
  """TEXT => ?where=column:value | NUMBER => ?eq=column:value"""
  for item in filter_list(b.where):
    col, val = parse_item(item)
    q = q.having(get_column(model, col) == val)
  for item in filter_list(b.eq):
    col, val = parse_item(item)
    q = q.having(get_column(model, col) == to_number(val))
  return q

def query_isnot(b, model, q):
  """TEXT => ?isnot=column:value | NUMBER => ?noteq=column:value"""
  for item in filter_list(b.isnot):
    col, val = parse_item(item)
    q = q.having(get_column(model, col) != val)
  for item in filter_list(b.noteq):
    col, val = parse_item(item)
    q = q.having(get_column(model, col) != to_number(val))
  return q

def query_like(b, model, q):
  """TEXT_ONLY => ?like=column:value"""
  BOOL_MAP = {"true": True, "false": False, "null": None, "notnull": "NOTNULL"}

  for item in filter_list(b.like):
    col, raw_val = parse_item(item)

    if raw_val in BOOL_MAP:
      mapped = BOOL_MAP[raw_val]
      col_expr = get_column(model, col)
      q = q.having(col_expr.isnot(None)) if raw_val == "notnull" else q.having(col_expr.is_(mapped))
    else:
      q = q.having(get_column(model, col).ilike(f"%{raw_val}%"))

  return q

def query_notlike(b, model, q):
  """TEXT_ONLY => ?notlike=column:value"""
  for item in filter_list(b.notlike):
    col, val = parse_item(item)
    q = q.having(get_column(model, col).notilike(f"%{val}%"))
  return q

def query_start(b, model, q):
  """TEXT_ONLY => ?start=column:value"""
  for item in filter_list(b.start):
    col, val = parse_item(item)
    q = q.having(get_column(model, col).ilike(f"{val}%"))
  return q

def query_end(b, model, q):
  """TEXT_ONLY => ?end=column:value"""
  for item in filter_list(b.end):
    col, val = parse_item(item)
    q = q.having(get_column(model, col).ilike(f"%{val}"))
  return q

def query_in(b, model, q):
  """ALL => ?in_=column:value1,value2"""
  for item in filter_list(b.in_):
    col, val = parse_item(item)
    vals = [x.strip() for x in val.split(",")]
    q = q.having(get_column(model, col).in_(vals))
  return q

def query_between(b, model, q):
  """ALL => ?between=column:value1 to value2"""
  for item in filter_list(b.between):
    col, val = parse_item(item)
    start, end = val.split(" to ", 1)
    q = q.having(get_column(model, col).between(start, end))
  return q

def query_notbetween(b, model, q):
  """ALL => ?notbetween=column:value1 to value2"""
  for item in filter_list(b.notbetween):
    col, val = parse_item(item)
    start, end = val.split(" to ", 1)
    q = q.having(not_(get_column(model, col).between(start, end)))
  return q

def query_gt(b, model, q):
  for item in filter_list(b.gt):
    col, val = parse_item(item)
    q = q.having(get_column(model, col) > to_number(val))
  return q

def query_gte(b, model, q):
  for item in filter_list(b.gte):
    col, val = parse_item(item)
    q = q.having(get_column(model, col) >= to_number(val))
  return q

def query_lt(b, model, q):
  for item in filter_list(b.lt):
    col, val = parse_item(item)
    q = q.having(get_column(model, col) < to_number(val))
  return q

def query_lte(b, model, q):
  for item in filter_list(b.lte):
    col, val = parse_item(item)
    q = q.having(get_column(model, col) <= to_number(val))
  return q

def query_trash(b, model, q):
  if "deleted_at" in model:
    col = get_column(model, "deleted_at")
    if b.trash: q = q.having(col.isnot(None))
    elif not b.all: q = q.having(col.is_(None))
  return q

def query_order(b, model, q):
  if b.order:
    col, order = parse_item(b.order)
    col_expr = get_column(model, col)
    q = q.order_by(col_expr.asc() if order.lower() == "asc" else col_expr.desc())
  return q

def query_all(browse_queries, model, query=None):
  q = query if query is not None else select()

  FILTERS = [
    ("where", query_where),
    ("isnot", query_isnot),
    ("like", query_like),
    ("notlike", query_notlike),
    ("start", query_start),
    ("end", query_end),
    ("in", query_in),
    ("gt", query_gt),
    ("gte", query_gte),
    ("lt", query_lt),
    ("lte", query_lte),
    ("between", query_between),
    ("notbetween", query_notbetween),
    ("trash", query_trash),
    ("order", query_order),
  ]

  for name, fn in FILTERS:
    try:
      q = fn(browse_queries, model, q)
    except Exception as e:
      raise BadRequest400(f"Error in '{name}' filter: {str(e)}", e)

  return q
