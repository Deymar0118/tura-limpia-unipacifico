import os
import sys
from logging.config import fileConfig

from alembic import context
from dotenv import load_dotenv
from sqlalchemy import engine_from_config, pool

# Cargar variables de entorno
load_dotenv()

# Agregar la raíz del proyecto al PATH para resolver importaciones desde 'src'
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# 1. Importar la clase Base oficial del proyecto
from src.core.database import Base

# 2. Cargar el paquete de modelos oficiales para registrar las 16 tablas en Base.metadata
import src.models

config = context.config

# 3. Leer y normalizar la URL para conectividad síncrona en Alembic
db_url = os.getenv("DATABASE_URL", "")
if db_url.startswith("postgresql+asyncpg://"):
    db_url = db_url.replace("postgresql+asyncpg://", "postgresql://")

config.set_main_option("sqlalchemy.url", db_url)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()