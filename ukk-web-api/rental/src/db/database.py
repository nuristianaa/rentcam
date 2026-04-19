
from config import getenv
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from utils.responses import BadRequest400

# BASE DATABASE URL RESOLVER
DATABASE_URL = getenv('DATABASE_URL') or getenv('DATABASE_PUBLIC_URL')
if DATABASE_URL:
  # SQLAlchemy 1.4+ requires postgresql:// instead of postgres://
  DB_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
else:
  DB_URL = f"postgresql://{getenv('DB_USER')}:{getenv('DB_PASSWORD')}@{getenv('DB_HOST')}/{getenv('DB_NAME')}"

engine = create_engine(
  DB_URL,
  pool_size=10,      # default 5
  max_overflow=20,   # default 10
  pool_timeout=30,   # seconds
  pool_recycle=1800, # recycle every 30 min
)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
  db = Session()
  try:
    yield db
  except SQLAlchemyError as e:
    db.rollback()
    print("DB exception:", str(e))
    raise BadRequest400(str(e)) from e
  finally:
    db.close()


#---------- ASYNC MAIN ----------#
if DATABASE_URL:
  DB_ASYNC_URL = DATABASE_URL.replace("postgres://", "postgresql+asyncpg://", 1).replace("postgresql://", "postgresql+asyncpg://", 1)
else:
  DB_ASYNC_URL = f"postgresql+asyncpg://{getenv('DB_USER')}:{getenv('DB_PASSWORD')}@{getenv('DB_HOST')}/{getenv('DB_NAME')}"

main_async_engine = create_async_engine(
  DB_ASYNC_URL,
  echo=False,
  pool_size=10,
  max_overflow=20,
  pool_timeout=30,    # ⏳ Optional but safer under load
  pool_recycle=1800,  # 🔁 Avoid stale connections (30 minutes)
  pool_pre_ping=True  # 🩺 Detect broken connections automatically
)
MainAsyncSession = async_sessionmaker(bind=main_async_engine, autoflush=False, expire_on_commit=False)

async def get_async_db():
  async with MainAsyncSession() as session:
    try:
      yield session
    except SQLAlchemyError as e:
      await session.rollback()
      print('DB exception:', str(e))
      raise BadRequest400(str(e))
    finally:
      await session.close()


#---------- LOG ----------#
log_engine = create_engine(
  DB_URL,
  pool_size=10,      # default 5
  max_overflow=20,   # default 10
  pool_timeout=30,   # seconds
  pool_recycle=1800, # recycle every 30 min
)
LogSession = sessionmaker(autocommit=False, autoflush=False, bind=log_engine)

def get_db_log():
  db = LogSession()
  try:
    yield db
  except SQLAlchemyError as e:
    print("DB exception:", str(e))
    raise BadRequest400(str(e)) from e
  finally:
    db.close()


#---------- ASYNC LOG ----------#
log_async_engine = create_async_engine(
  DB_ASYNC_URL,
  echo=False,
  pool_size=10,
  max_overflow=20,
  pool_timeout=30,    # ⏳ Optional but safer under load
  pool_recycle=1800,  # 🔁 Avoid stale connections (30 minutes)
  pool_pre_ping=True  # 🩺 Detect broken connections automatically
)
LogAsyncSession = async_sessionmaker(bind=log_async_engine, autoflush=False, expire_on_commit=False)

async def get_async_db_log():
  async with LogAsyncSession() as session:
    try:
      yield session
    except SQLAlchemyError as e:
      await session.rollback()
      print('DB exception:', str(e))
      raise BadRequest400(str(e))
    finally:
      await session.close()