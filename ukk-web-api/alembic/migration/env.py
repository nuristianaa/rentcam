from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv, dotenv_values
load_dotenv()
cfg_env = dotenv_values(".env")

# Priority 1: Check for DATABASE_URL or DATABASE_PUBLIC_URL
DATABASE_URL = cfg_env.get('DATABASE_URL') or cfg_env.get('DATABASE_PUBLIC_URL')
if DATABASE_URL:
    DB_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
else:
    # Priority 2: Traditional individual variables
    DB_URL = f"postgresql://{cfg_env.get('DB_USER', 'postgres')}:{cfg_env.get('DB_PASSWORD', '')}@{cfg_env.get('DB_HOST', 'localhost')}/{cfg_env.get('DB_NAME', 'postgres')}"

engine = create_engine(DB_URL)

Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
config.set_main_option(
    "sqlalchemy.url",
    DB_URL,
)

fileConfig(config.config_file_name)


target_metadata = Base.metadata


def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
