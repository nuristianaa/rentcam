from config import is_dev
from fastapi import Query
from pydantic import BaseModel, Field

SHOW_DOCS = is_dev()

class BulkId(BaseModel):
  id: list[int | str] | None = []


class BrowseSchema(BaseModel):
  """
  Base Query Parameter with additional parameter
  """
  group_select  : str | None = None
  pivot         : list[str] | None  = None
  summary       : bool | None = None
  summary_map   : list[str] | None = []

  table         : bool       = False
  limit         : int        = Field(10, ge=0)
  page          : int        = Field(1, ge=1)
  trash         : bool       = False
  all           : bool       = False
  order         : str | None = None
  where         : list[str] | None = None # text
  isnot         : list[str] | None = None # text
  like          : list[str] | None = None # text
  notlike       : list[str] | None = None # text
  start         : list[str] | None = None # text
  end           : list[str] | None = None # text
  between       : list[str] | None = None # all
  notbetween    : list[str] | None = None # all
  in_           : list[str] | None = None # all
  eq            : list[str] | None = None # date, number
  noteq         : list[str] | None = None # date, number
  gt            : list[str] | None = None # date, number
  gte           : list[str] | None = None # date, number
  lt            : list[str] | None = None # date, number
  lte           : list[str] | None = None # date, number


def browse_query(
  group_select: str | None = Query(None,      include_in_schema=SHOW_DOCS, description="[BROWSE] Autocomplete, select by single column and return list group by this column."),
  pivot: list[str] | None  = Query(None,      include_in_schema=SHOW_DOCS, examples=['net_0:avg,sum,min,max', 'net_1:sum'], description="[BROWSE] Pivot based on data query (return ): sum,avg,min,max."),
  summary: bool | None     = Query(None,      description="enable for get summary per column"),
  summary_map: list[str] | None = Query(None, description="columns list that what to summarize (avg, sum, min, max, count), e.g. rit:avg"),


  table     : bool       = Query(False,      include_in_schema=SHOW_DOCS, description="[BROWSE] Return table format: total & items."),
  limit     : int        = Query(10, ge=0,   include_in_schema=SHOW_DOCS, description="[BROWSE] Apply Limit."),
  page      : int        = Query(1, ge=1,    include_in_schema=SHOW_DOCS, description="[BROWSE] Pagination page."),
  trash     : bool       = Query(False,      include_in_schema=SHOW_DOCS, description="[BROWSE] Show only deleted rows."),
  all       : bool       = Query(False,      include_in_schema=SHOW_DOCS, description="[BROWSE] Show all rows (ignore trash)."),

  order     : str | None       = Query(None, include_in_schema=SHOW_DOCS, examples=["created_at:desc"], description="[BROWSE] Ordering by, only implement one order."),
  where     : list[str] | None = Query(None, include_in_schema=SHOW_DOCS, examples=["code:ABC"], description="[BROWSE] text only, search exactly 'val'"),
  isnot     : list[str] | None = Query(None, include_in_schema=SHOW_DOCS, examples=["code:ABC"], description="[BROWSE] text only, search exactly not 'val'"),
  like      : list[str] | None = Query(None, include_in_schema=SHOW_DOCS, examples=["code:ABC", "code:null", "code:notnull", "is_active:true", "is_active:false"], description="[BROWSE] textonly, insensitive case search '%val%'"),
  notlike   : list[str] | None = Query(None, include_in_schema=SHOW_DOCS, examples=["code:ABC"], description="[BROWSE] text only, insensitive case search notlike '%val%'"),
  start     : list[str] | None = Query(None, include_in_schema=SHOW_DOCS, examples=["code:ABC"], description="[BROWSE] text only, insensitive case search 'val%'"),
  end       : list[str] | None = Query(None, include_in_schema=SHOW_DOCS, examples=["code:001"], description="[BROWSE] text only, insensitive case search '%val'"),

  between   : list[str] | None = Query(None, include_in_schema=SHOW_DOCS, examples=["date:2025-01-01 to 2025-12-31"], description="[BROWSE] between = column:value1 to value2"),
  notbetween: list[str] | None = Query(None, include_in_schema=SHOW_DOCS, examples=["date:2025-01-01 to 2025-12-31"], description="[BROWSE] not Between = column:value1 to value2"),
  in_       : list[str] | None = Query(None, include_in_schema=SHOW_DOCS, examples=["code:ABC,DEF,GHI"], description="[BROWSE] in = column:value1,value2"),

  gt        : list[str] | None = Query(None, include_in_schema=SHOW_DOCS, examples=["qty:100", "date:2025-01-01"], description="[BROWSE] number or date, greater than"),
  gte       : list[str] | None = Query(None, include_in_schema=SHOW_DOCS, examples=["qty:100", "date:2025-01-01"], description="[BROWSE] number or date, greater than equal"),
  lt        : list[str] | None = Query(None, include_in_schema=SHOW_DOCS, examples=["qty:100", "date:2025-01-01"], description="[BROWSE] number or date, lower than"),
  lte       : list[str] | None = Query(None, include_in_schema=SHOW_DOCS, examples=["qty:100", "date:2025-01-01"], description="[BROWSE] number or date, lower than equal"),
  eq        : list[str] | None = Query(None, include_in_schema=SHOW_DOCS, examples=["qty:100", "date:2025-01-01"], description="[BROWSE] number or date, equal"),
  noteq     : list[str] | None = Query(None, include_in_schema=SHOW_DOCS, examples=["qty:100", "date:2025-01-01"], description="[BROWSE] number or date, not equal"),
) -> BrowseSchema:
  """
  Create parameters schema for API
  """
  return BrowseSchema(
    group_select = group_select,
    pivot        = pivot,
    summary      = summary,
    summary_map  = summary_map,

    table        = table,
    limit        = limit,
    page         = page,
    trash        = trash,
    all          = all,
    order        = order,

    where        = where,
    isnot        = isnot,
    like         = like,
    notlike      = notlike,
    start        = start,
    end          = end,
    between      = between,
    notbetween   = notbetween,
    in_          = in_,
    gt           = gt,
    gte          = gte,
    lt           = lt,
    lte          = lte,
    eq           = eq,
    noteq        = noteq,
  )
