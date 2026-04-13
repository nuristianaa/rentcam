from collections.abc import Mapping

from utils.responses import BadRequest400

AGG_FUNCS = {
  "sum": lambda values: sum(values),
  "avg": lambda values: sum(values) / len(values) if values else None,
  "min": lambda values: min(values) if values else None,
  "max": lambda values: max(values) if values else None,
}

# ===================
# Helpers
# ===================
def parse_item(item: str) -> tuple[str, str]:
  """Split 'column:value' safely."""
  if ":" not in item:
    raise BadRequest400(f"Invalid format '{item}'. Expected 'column:value'")
  col, val = item.split(":", 1)
  return col, val

def to_number(val: str):
  """Convert to float if possible."""
  try:
    return float(val)
  except:
    return val

def get_column(model: Mapping, col: str):
  """Get SQLAlchemy model column safely."""
  col_obj = model.get(col) if isinstance(model, Mapping) else getattr(model, col, None)
  if col_obj is None:
    raise BadRequest400(f"There is no column named '{col}'")
  return col_obj

def filter_list(browse_list: list[str] | None):
  """Return list only if not empty."""
  return browse_list or []

def safe_number(value):
  """Convert to float; return 0 when invalid."""
  try:
    if value is None: return 0
    return float(value)
  except (TypeError, ValueError):
    return 0

def apply_pivot(rows: list[dict], pivots: list[str]):
  """
  Perform pivot/aggregate in Python.
  rows = list of dicts
  pivots = ["net_0:sum,avg", "net_1:sum"]
  """
  # Parse pivot syntax
  pivot_map = {}
  for p in pivots:
    col, ops = p.split(":")
    ops = ops.split(",")
    pivot_map[col] = ops

  result = {}
  for col, ops in pivot_map.items():
    # extract column values
    values = [safe_number(r[col]) for r in rows if r.get(col) is not None]
    result[col] = {}
    for op in ops:
      if op not in AGG_FUNCS:
        raise ValueError(f"Unsupported pivot op '{op}'")
      result[col][op] = AGG_FUNCS[op](values)
  return result
