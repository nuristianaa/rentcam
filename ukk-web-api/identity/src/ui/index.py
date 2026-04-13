from config import getenv
from fastapi import Request
from fastapi.templating import Jinja2Templates
from utils.helpers.date import format_date, millis2date
from utils.helpers.number_text import format_number


def render(*, path: str, request: Request, params: dict):
  ASSET_URL = getenv("PUBLIC_ASSET", "http://localhost:8090")
  templates = Jinja2Templates(directory="src", variable_start_string="[[", variable_end_string="]]")
  ver = 1.1
  templates.env.filters["format_number"] = format_number
  templates.env.filters["format_date"] = format_date
  templates.env.filters["millis2date"] = millis2date
  return templates.TemplateResponse(f"{path}", {"request": request, "params": params, "ver": ver, "app_url": ASSET_URL})
