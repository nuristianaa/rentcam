import asyncio
import contextlib
import os
from contextlib import asynccontextmanager

import uvicorn
from app.audit_trail.service_background import flush_audit_logs
from config import getenv, is_dev, origins
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError, ResponseValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles
from logger import logger
from logger_scheduler import logger_scheduler
from pydantic import BaseModel
from slowapi import Limiter
from slowapi.util import get_remote_address
from starlette.middleware.base import BaseHTTPMiddleware
from utils.helpers.date import currentmillis, now
from utils.producers.lifecycle import shutdown_queue, startup_queue

# AUTH
from app.audit_trail import routes as audit_trail
from app.auth import authentication
from app.auth.master_file import routes as master_file
from app.auth.notification import routes as notification
from app.auth.permission import routes as permission
from app.auth.role import routes as role
from app.auth.user import me_routes
from app.auth.user import routes as user

from utils.web_socket import ws_routes


from utils.responses import (
  BadRequest400,
  Forbidden403,
  NotFound404,
  Unauthorized401,
  rate_limit_exceeded_handler,
  res_content,
)


from db.database import Base, engine


# ==================================================================
# 🌱 Lifespan (Startup & Shutdown)
# ==================================================================
@asynccontextmanager
async def lifespan(app: FastAPI):
  print("🚀 FastAPI starting...")
  # Create tables automatically on startup
  try:
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created/verified.")
  except Exception as e:
    print(f"❌ Error creating tables: {e}")
  
  startup_queue()
  # Start background async tasks
  task1 = asyncio.create_task(flush_audit_logs())

  background_tasks = [task1]
  print("🔄 Starting background tasks...")

  try:
    yield
  finally:
    shutdown_queue()
    print("🛑 Shutting down background tasks...")
    # Cancel tasks
    for t in background_tasks:
      t.cancel()

    # Suppress CancelledError
    for t in background_tasks:
      with contextlib.suppress(asyncio.CancelledError):
        await t

    print("✅ Background tasks stopped cleanly.")

    print("✅ Lifespan shutdown complete.")


title = "IDENTITY API"
ver = "1.0.0"
app = FastAPI(title=title, lifespan=lifespan, debug=is_dev())


# ==================================================================
# ⚙️ Rate Limiter Configuration
# ==================================================================
# from slowapi.errors import RateLimitExceeded
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(429, rate_limit_exceeded_handler)  # type: ignore


# ==================================================================
# 🧱 Core Routes
# ==================================================================
@app.get("/")
@limiter.limit("5/minute")  # Allow 5 requests per minute
def read_root(request: Request):
  return {"app": title, "ver": ver, "datetime": now(), "currentmillis": currentmillis()}


@app.get("/healthz", response_class=PlainTextResponse)
def healthz():
  return "OK"

class ReqLog(BaseModel):
  message: str

@app.post("/logger-scheduler", response_class=PlainTextResponse)
@limiter.limit("1/second")
def logger_info(request: Request, req: ReqLog):
  logger_scheduler.info(req.message)
  return 'success'


# ==================================================================
# 🧩 STATIC FILES
# ==================================================================
static_dir = os.path.join("src", "ui", "assets")
if not os.path.exists(static_dir):
    # Try alternative path if main one fails
    static_dir = os.path.join(os.path.dirname(__file__), "ui", "assets")

if os.path.exists(static_dir):
    app.mount("/ui", StaticFiles(directory=static_dir), name="ui")
else:
    print(f"⚠️ Warning: Static directory '{static_dir}' not found. Skipping mount to prevent crash.")



# ==================================================================
# 🧩 Routers
# ==================================================================

# AUTH
# app.include_router(generator.router)
app.include_router(authentication.router)
app.include_router(me_routes.router)
app.include_router(user.router)
app.include_router(permission.router)
app.include_router(role.router)
app.include_router(master_file.router)
app.include_router(notification.router)
app.include_router(audit_trail.router)



# ==================================================================
# 🧱 Web Socket
# ==================================================================
app.include_router(ws_routes.router)


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
  return JSONResponse(status_code=422, content=res_content(request, 404, "Validation Error", exc.errors()))


# ==================================================================
# 🛡️ Security Middleware
# ==================================================================
class SecurityHeadersMiddleware(BaseHTTPMiddleware):
  async def dispatch(self, request: Request, call_next):
    response = await call_next(request)
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains; preload"
    # response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"
    return response


# ==================================================================
# 🧰 Middleware Registration Order
# ==================================================================
app.add_middleware(SecurityHeadersMiddleware)
@app.middleware("http")
async def add_timing(request, call_next):
  import time
  start = time.time()
  response = await call_next(request)
  duration = (time.time() - start) * 1000
  response.headers["X-Process-Time-ms"] = str(round(duration, 2))
  return response
app.add_middleware(
  CORSMiddleware,
  allow_origins=origins,
  allow_credentials=True,
  allow_methods=["*"],  # ['GET','PUT','POST','DELETE','PATCH','HEAD','OPTIONS'],
  allow_headers=["*"],
)


# ==================================================================
# 🏁 Run Server
# ==================================================================
if __name__ == "__main__":
  uvicorn.run(
    "main:app",
    host=getenv("HOST", "0.0.0.0"),
    port=int(getenv("PORT", getenv("PORT_IDENTITY", "8090"))),
    reload=is_dev(),
    workers=1 if is_dev() else 4,
    limit_concurrency=100,
    timeout_keep_alive=5,
  )
  