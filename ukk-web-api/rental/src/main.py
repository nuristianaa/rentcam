import os
from contextlib import asynccontextmanager

import uvicorn
from config import getenv, is_dev, origins
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError, ResponseValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles
from db.database import Base, engine
from logger import logger
from utils.helpers.date import currentmillis, now
from utils.responses import (
  BadRequest400,
  Forbidden403,
  NotFound404,
  Unauthorized401,
  res_content,
)


# ==================================================================
# 🌱 Lifespan (Startup & Shutdown)
# ==================================================================
@asynccontextmanager
async def lifespan(app: FastAPI):
  print("🚀 Rental API starting...")
  # Create tables automatically on startup
  try:
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created/verified.")
  except Exception as e:
    print(f"❌ Error creating tables: {e}")
  
  try:
    yield
  finally:
    print("✅ Lifespan shutdown complete.")


title = "Rental Foto API"
ver = "1.0.0"
app = FastAPI(title=title, lifespan=lifespan, debug=is_dev())


# ==================================================================
# 🧱 Core Routes
# ==================================================================
@app.get("/")
def read_root(request: Request):
  return {"app": title, "ver": ver, "datetime": now(), "currentmillis": currentmillis()}


@app.get("/healthz", response_class=PlainTextResponse)
def healthz():
  return "OK"


# ==================================================================
# 🧩 STATIC FILES
# ==================================================================
root_dir = os.path.dirname(__file__)
static_dir = os.path.join(root_dir, "..", "static_files")

# Ensure static_files exists
if not os.path.exists(static_dir):
  os.makedirs(static_dir)

app.mount("/ui", StaticFiles(directory=os.path.join(root_dir, "ui", "assets")), name="ui")
app.mount("/static_files", StaticFiles(directory=static_dir), name="static_files")


# ==================================================================
# 🧩 Routers
# ==================================================================
from app.master.item_categories import routes as item_categories_routes
from app.master.items import routes as items_routes
from app.transaction.rentals import routes as rentals_routes
from app.transaction.rental_items import routes as rental_items_routes
from app.transaction.payments import routes as payments_routes
from app.transaction.reviews import routes as reviews_routes
from app.transaction.rental_checkpoints import routes as rental_checkpoints_routes
from app.transaction.rentals_histories import routes as rentals_histories_routes
from app.transaction.invoice import routes as invoice_routes


rental_routers = [
  # ── Master ──────────────────────────────
  item_categories_routes.router,
  items_routes.router,

  # ── Transaction ─────────────────────────
  rentals_routes.router,
  rental_items_routes.router,
  payments_routes.router,
  reviews_routes.router,
  rental_checkpoints_routes.router,
  rentals_histories_routes.router,
  invoice_routes.router,
]
for router in rental_routers: app.include_router(router)


# ==================================================================
# 🧱 Exception Handlers
# ==================================================================
@app.exception_handler(BadRequest400)
def bad_request(request: Request, exc: BadRequest400) -> JSONResponse:
  logger.error(f"[{request.method} {request.url.path}] {exc.name} {exc.detail}")
  return JSONResponse(status_code=400, content=res_content(request, 400, exc.name, exc.detail))


@app.exception_handler(Unauthorized401)
def unauthorize(request: Request, exc: Unauthorized401) -> JSONResponse:
  return JSONResponse(status_code=401, content=res_content(request, 401, exc.name))


@app.exception_handler(Forbidden403)
def forbidden(request: Request, exc: Forbidden403) -> JSONResponse:
  return JSONResponse(status_code=403, content=res_content(request, 403, exc.name))


@app.exception_handler(NotFound404)
def not_found(request: Request, exc: NotFound404) -> JSONResponse:
  return JSONResponse(status_code=404, content=res_content(request, 404, exc.name))


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
  return JSONResponse(status_code=406, content=res_content(request, 406, "Validation Error", exc.errors()))


@app.exception_handler(ResponseValidationError)
async def response_validation_exception_handler(request: Request, exc: ResponseValidationError) -> JSONResponse:
  return JSONResponse(status_code=422, content=res_content(request, 422, "Validation Error", exc.errors()))


# ==================================================================
# 🧰 Middleware
# ==================================================================
app.add_middleware(
  CORSMiddleware,
  allow_origins=origins,
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)


# ==================================================================
# 🏁 Run Server
# ==================================================================
if __name__ == "__main__":
  uvicorn.run(
    "main:app",
    host=getenv("HOST", "0.0.0.0"),
    port=int(getenv("PORT", getenv("PORT_RENTAL", "8100"))),
    reload=is_dev(),
    workers=1 if is_dev() else 4,
    limit_concurrency=100,
    timeout_keep_alive=5,
  )