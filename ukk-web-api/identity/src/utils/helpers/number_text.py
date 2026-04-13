import random
import re
import string
import unicodedata
from datetime import datetime
from typing import Any
from uuid import UUID


def randrange(fr: int = 1, to: int = 100) -> int:
  return random.randrange(fr, to, 3)

def gen_random_number(exclude: list[int]):
  r = random.randint(1, 99999)
  while r in exclude:
    r = random.randint(1, 99999)
  return r

def class2json(value: Any):
  return [
    value for key, value in value.__dict__.items()
    if not key.startswith('__') and isinstance(value, str | int)  # Only allow strings and integers
  ]
  # return [value for key, value in value.__dict__.items() if not key.startswith('__')]

def gen_code_date(prefix: str, format_date: str = '%y%m'):
  # Parameters
  date = datetime.now()

  # Format components
  yy_mm = date.strftime(format_date)  # e.g. "2512" for Dec 2025

  # Final code
  return f"{prefix}-{yy_mm}"

def gen_code(prefix: str, number: int, format_date: str = '%y%m'):
  number_str = f"{number:04d}"        # zero-padded to 4 digits: "0001"
  prefix_date = gen_code_date(prefix=prefix, format_date=format_date)

  # Final code
  return f"{prefix_date}{number_str}"

def format_number(value, precision=None, use_comma_decimal=False):
  if value is None:
    return None
  try:
    number = float(value)
  except (ValueError, TypeError):
    return None

  if precision is None:
    precision = 2  # Default precision

  formatted = f"{number:,.{precision}f}"

  if use_comma_decimal:
    # Replace "." with "," and "," with "." for European-style
    formatted = formatted.replace(",", "X").replace(".", ",").replace("X", ".")

  return formatted

def handler_number(value, precision=None, default_value = 0 ):
  if value is None:
    return default_value
  return format_number(value, precision)

def generate_random_string(length=12):
  characters = string.ascii_letters + string.digits  # A-Z, a-z, 0-9
  return ''.join(random.choice(characters) for _ in range(length))

def generate_strong_password(length=20):
    if length < 8:
        raise ValueError("Password must be at least 8 characters long")

    # Ensure all character types are included
    upper = random.choice(string.ascii_uppercase)
    lower = random.choice(string.ascii_lowercase)
    digit = random.choice(string.digits)
    special = random.choice("!@#$%^&*()-_=+[]{};:,.<>?")

    # Fill the rest with random choices from all character sets
    all_chars = string.ascii_letters + string.digits + "!@#$%^&*()-_=+[]{};:,.<>?"
    remaining = [random.choice(all_chars) for _ in range(length - 4)]

    # Combine and shuffle
    password_list = list(upper + lower + digit + special) + remaining
    random.shuffle(password_list)

    return ''.join(password_list)

def convert_uuid(obj):
  if isinstance(obj, dict):
    return {k: convert_uuid(v) for k, v in obj.items()}
  elif isinstance(obj, list):
    return [convert_uuid(v) for v in obj]
  elif isinstance(obj, UUID):
    return str(obj)
  else:
    return obj

def slugify(text: str|None, separator: str = "_") -> str:
  if text is None: text = ''
  if separator not in ("_", "-"):
    raise ValueError("Separator must be '_' or '-'")

  text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
  text = text.lower()
  text = re.sub(r"[^\w\s-]", "", text)
  text = re.sub(r"[\s" + ("_" if separator == "-" else "-") + r"]+", separator, text)
  return text.strip(separator)

def divide_or_zero(numerator, denominator):
  """Return numerator/denominator safely, avoiding ZeroDivisionError."""
  try:
    return numerator / denominator if denominator != 0 else 0
  except (TypeError, ZeroDivisionError):
    return 0
