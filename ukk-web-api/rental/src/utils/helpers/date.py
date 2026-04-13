import calendar
import time
from collections.abc import ValuesView
from datetime import UTC, datetime, timedelta
from datetime import date as dtdate
from datetime import time as dttime

from config import getenv
from dateutil import parser
from num2words import num2words


def parse_date(date_str: str|datetime|None) -> datetime:
  """Parse date string or return if already datetime"""
  if isinstance(date_str, datetime): return date_str
  if date_str and str(date_str).strip() != '': return parser.parse(str(date_str))
  return datetime.now()

def to_date(alldate: str|datetime|dtdate)-> dtdate:
  if   isinstance(alldate, str): alldate      = datetime.strptime(alldate, "%Y-%m-%d").date()
  elif isinstance(alldate, datetime): alldate = alldate.date()
  return alldate

def today(diff: int = 0, format: str ="%Y-%m-%d") -> str:
  """Get Date Now"""
  timezone = int(getenv('TIMEZONE', '+0'))
  x   = datetime.now() + timedelta(hours = timezone)
  xx  = None
  if diff > 0: xx = x + timedelta(days = diff)
  elif diff < 0: xx = x - timedelta(days = diff*-1)
  if xx : return xx.strftime(format)
  else  : return x.strftime(format)

def now(diff: int = 0, format: str ="%Y-%m-%d %H:%M:%S") -> str:
  """Get Time Now"""
  timezone = int(getenv('TIMEZONE', '+0'))
  x   = datetime.now() + timedelta(hours = timezone)
  xx  = None
  if diff > 0: xx = x + timedelta(minutes= diff)
  elif diff < 0: xx = x - timedelta(minutes = diff*-1)
  if xx : return xx.strftime(format)
  else  : return x.strftime(format)

def format_date(date_: str|dtdate|dttime, format_to: str = "%Y-%m-%d", format_fr: str = None ) -> str: # type: ignore
  """Format date from typedate or string date to string date."""
  if isinstance(date_, str) and format_fr:
    dt = datetime.strptime(date_, format_fr)
  elif isinstance(date_, dtdate|dttime):
    dt = datetime.combine(date_, dttime()) if isinstance(date_, dtdate) else date_
  else:
    return ''
  return dt.strftime(format_to)

def format_date_period(d1: str|dtdate|None, d2: str|dtdate|None) -> str:
  """Format dua tanggal menjadi periode seperti '1 - 15 Oct 2025'."""
  if not d1 or not d2:
      return ''

  # Gunakan format_date() untuk ubah ke format konsisten
  d1_str = format_date(d1, "%Y-%m-%d")
  d2_str = format_date(d2, "%Y-%m-%d")

  if not d1_str or not d2_str:
      return ''

  d1_obj = datetime.strptime(d1_str, "%Y-%m-%d").date()
  d2_obj = datetime.strptime(d2_str, "%Y-%m-%d").date()

  month_names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                  "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

  d1_day = d1_obj.day
  d2_day = d2_obj.day
  d1_month = month_names[d1_obj.month - 1]
  d2_month = month_names[d2_obj.month - 1]
  d1_year = d1_obj.year
  d2_year = d2_obj.year

  # Bulan & tahun sama → "1 - 15 Oct 2025"
  if d1_obj.month == d2_obj.month and d1_obj.year == d2_obj.year:
    return f"{d1_day} - {d2_day} {d2_month} {d2_year}"

  # Tahun sama tapi bulan beda → "25 Sep - 5 Oct 2025"
  if d1_obj.year == d2_obj.year:
    return f"{d1_day} {d1_month} - {d2_day} {d2_month} {d2_year}"

  # Beda tahun → "25 Dec 2024 - 5 Jan 2025"
  return f"{d1_day} {d1_month} {d1_year} - {d2_day} {d2_month} {d2_year}"

#------- TIMEMILLIS -------#
def currentmillis() -> int:
  """Current timemillis."""
  return int(round(time.time() * 1000))

def date2millis(dt: datetime, timezone: int =7) -> int:
  """Convert datetime to timemillis."""
  try:
    timez = timezone * -1
    # dt = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    seconds = dt.replace(tzinfo=UTC).timestamp()
    seconds += timez * 60 * 60
    return int(round(seconds * 1000))
  except:
    return int(round(time.time() * 1000))

def millis2date(ms: int|str, timezone=7, format: str|None = None) -> str|datetime:
  """Convert timemillis to date."""
  seconds = round(int(ms)/1000.0)
  seconds += timezone * 60 * 60
  x = datetime.fromtimestamp(timestamp=seconds, tz=UTC) # type: ignore
  if format:
    return x.strftime(format)
  return x

#------- MATH OF DATES -------#
def days_diff_datetime(date1: dtdate, date2: dtdate, rounding: int = 2):
  """Return float total days."""
  diff_in_seconds = (date2 - date1).total_seconds()
  return round(diff_in_seconds/(24*60*60), rounding)

def days_diff(fr: str|dtdate, to: str|dtdate, format = "%Y-%m-%d") -> int:
  """Count day from 2 days for string or date type."""
  if type(fr) is str: start = datetime.strptime(fr, format)
  elif type(fr) is dtdate: start = fr
  if type(to) is str: end = datetime.strptime(to, format)
  elif type(to) is dtdate: end = to
  diff = end-start if end > start else start-end # type: ignore
  return diff.days

def minutes_between_datetimes(dt_str1: str, dt_str2: str):
  """Count minutes from 2 days for string type."""
  datetime_format = "%Y-%m-%d %H:%M:%S"
  # Convert the datetime strings to datetime objects
  dt_obj1 = datetime.strptime(dt_str1, datetime_format)
  dt_obj2 = datetime.strptime(dt_str2, datetime_format)

  # Calculate the time difference between the two datetimes
  time_difference = abs(dt_obj2 - dt_obj1)

  # Get the total number of minutes from the time difference
  total_minutes = time_difference.total_seconds() / 60

  return total_minutes

def add_date(date_: str|dtdate, days: int = 1, format: str = "%Y-%m-%d") -> str|None:
  """
    Add or subtract a number of days to a date.
    Parameters:
        date_ (str|datetime.date): The starting date, as a string or date object.
        days (int): Number of days to add (use negative for past dates).
        format (str): Format for parsing and returning date strings.
    Returns:
        str|None: The resulting date as a formatted string, or None if input is invalid.
  """
  try:
    start = datetime.strptime(date_, format) if isinstance(date_, str) else date_
    result_date = start + timedelta(days=days)
    return result_date.strftime(format)
  except Exception:
    return None

def get_last_day(date_str: str|None = None, date_format: str = '%Y-%m-%d') -> int:
  """Get last day on the date month. Format date string. Default None for today."""
  date_obj = datetime.strptime(date_str, date_format) if date_str else datetime.now()
  last_day = calendar.monthrange(date_obj.year, date_obj.month)[1]
  return last_day

def get_min_date(dates: list[str|dtdate|datetime|None]):
  min_stock_date = None
  for dt in dates:
    if dt and min_stock_date is None                      : min_stock_date = str(dt)
    if dt and min_stock_date and min_stock_date > str(dt) : min_stock_date = str(dt)
  return min_stock_date

def get_range_date(from_date: str, to_date:str)->list:
  # Convert strings to datetime objects
  start_date = datetime.strptime(from_date, "%Y-%m-%d")
  end_date = datetime.strptime(to_date, "%Y-%m-%d")

  # Generate all dates between start_date and end_date
  date_list = []
  while start_date <= end_date:
      date_list.append(start_date.strftime("%Y-%m-%d"))  # Format as string
      start_date += timedelta(days=1)

  return date_list

def get_shift_code(shifts, target_time):
  """
  Finds the correct shift code for a given time object.

  Args:
    shifts: The list of shift dictionaries.
    target_time: A datetime.time object to check.

  Returns:
    The matching shift code string or None.
  """
  for shift in shifts:
    start_time = datetime.strptime(shift['start'], "%H:%M").time()
    print(target_time)

    if shift['end'] == '24:00':
      if target_time >= start_time:
        return shift['code']

    else:
      end_time = datetime.strptime(shift['end'], "%H:%M").time()
      if start_time <= target_time < end_time:
        return shift['code']

  return None

#------- FOR QUERY PARTITION -------#
def transform_query_partition(date_columns: list[str], query_list: ValuesView[str]):
  date_from: str = today(-100)
  date_to: str = today(+1)
  for v in query_list:
    try:
      if v.find(':') > -1:
        [idx, value] = v.split(':')
        if idx in date_columns:
          fr = value
          to = value
          if value.find(' to ') > -1: [fr, to] = value.split(' to ')
          try:
            fr = millis2date(fr, 7, '%Y-%m-%d')
            to = millis2date(to, 7, '%Y-%m-%d')
          except: ''
          if fr and to and type(fr) is str and type(to) is str:
            fr = add_date(fr, -100)
            to = add_date(to, 100)
            if fr and fr < date_from: date_from = fr
            if to and to > date_to: date_to = to
            # print(date_from, date_to)
    except Exception as e:
      print('[INFO] transform_query_partition: ', e, f'{date_from} to {date_to}')
  return date_from, date_to

def extract_reqdate(req_date: str|None) -> tuple[str, str]:
  start = today()
  end = today()
  if req_date:
    [start, end] = req_date.split(" to ") if req_date.find(' to ') > -1 else [req_date, req_date]
  return start, end

#------- OTHER FORMATTING & TRANSFORMING -------#
INDONESIAN_WEEKDAYS = [
  "Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"
]
INDONESIAN_MONTHS = [
  "", "Januari", "Februari", "Maret", "April", "Mei", "Juni",
  "Juli", "Agustus", "September", "Oktober", "November", "Desember"
]

def format_date_to_indonesian_text(date: dtdate, mode: str = 'all') -> str:
  weekday = INDONESIAN_WEEKDAYS[date.weekday()]
  day_text = num2words(date.day, lang='id').capitalize()
  month_text = INDONESIAN_MONTHS[date.month]
  year_text = num2words(date.year, lang='id').title()
  if (mode == 'date'): weekday = ''
  return f"{weekday} tanggal {day_text} bulan {month_text} tahun {year_text}"

def format_date_id_dmy(date: dtdate) -> str:
    day = date.day
    month = INDONESIAN_MONTHS[date.month]
    year = date.year
    return f"{day} {month} {year}"

def format_date_id_my(date: dtdate) -> str:
    month = INDONESIAN_MONTHS[date.month]
    year = date.year
    return f"{month} {year}"

def format_date_range(date_0: str|dtdate, date_1: str|dtdate) -> str:
  start = datetime.strptime(date_0, "%Y-%m-%d").date() if isinstance(date_0, str) else date_0
  end = datetime.strptime(date_1, "%Y-%m-%d").date() if isinstance(date_1, str) else date_1

  # Same exact date → "20 Dec 25"
  if start == end:
    return start.strftime("%-d %b %y")
  # Same year and month → "2–20 Dec 25"
  if start.year == end.year and start.month == end.month:
    return f"{start.day}–{end.day} {end.strftime('%b %y')}"
  # Same year but different month → "1 Jan–20 Dec 25"
  if start.year == end.year:
    return f"{start.day} {start.strftime('%b')}–{end.day} {end.strftime('%b %y')}"
  # Different years → "1 Feb 24–20 Dec 25"
  return f"{start.day} {start.strftime('%b %y')}–{end.day} {end.strftime('%b %y')}"

def make_label_period (start_date: str|dtdate|None, end_date: str|dtdate|None) ->dict:
  today = datetime.today().date()

  # Convert string → date
  def to_date(d: str|dtdate|None) -> dtdate:
    if isinstance(d, str):
      try: return datetime.strptime(d, "%Y-%m-%d").date()
      except ValueError: return today
    return d or today

  start_date = to_date(start_date)
  end_date = to_date(end_date)

  def format_date_period(sd: dtdate, ed: dtdate) -> str:
    if sd.year == ed.year:
      if sd.month == ed.month:
        return f"{sd.day} - {ed.day} {ed.strftime('%b %Y')}"
      return f"{sd.strftime('%d %b')} - {ed.strftime('%d %b %Y')}"
    return f"{sd.strftime('%d %b %Y')} - {ed.strftime('%d %b %Y')}"

  # Daily
  if start_date == end_date == today:
    label_daily = "Today"
  elif start_date == end_date:
    label_daily = start_date.strftime("%d %b %Y")
  else:
    label_daily = format_date_period(start_date, end_date)

  # MTD
  if start_date.month == end_date.month and start_date.year == end_date.year:
    label_mtd = f"1 - {end_date.day} {end_date.strftime('%b %Y')}"
  else:
    label_mtd = format_date_period(start_date, end_date)

  # YTD
  if start_date.year == end_date.year:
    label_ytd = f"Jan - {end_date.strftime('%b %Y')}"
  else:
    label_ytd = f"{start_date.strftime('%b %Y')} - {end_date.strftime('%b %Y')}"

  return {
    "daily": label_daily,
    "mtd": label_mtd,
    "ytd": label_ytd,
  }
  
def get_month_range(start_date: str|None, end_date: str|None):
  if not start_date or not end_date:
    return []

  start_dt = dtdate.fromisoformat(f"{start_date}-01")
  end_year, end_month = map(int, end_date.split("-"))
  end_dt = dtdate(end_year, end_month, 1)

  current_dt = start_dt
  months = []
  while current_dt <= end_dt:
    months.append((current_dt.year, current_dt.month))
    if current_dt.month == 12:
      current_dt = dtdate(current_dt.year + 1, 1, 1)
    else:
      current_dt = dtdate(current_dt.year, current_dt.month + 1, 1)

  return months
