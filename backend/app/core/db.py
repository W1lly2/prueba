# app/core/db.py
from contextlib import asynccontextmanager
from psycopg_pool import AsyncConnectionPool
from psycopg.rows import dict_row
from app.core.config import DBSettings

_db = DBSettings()

# DSN limpio, sin query params
DSN = f"postgresql://{_db.user}:{_db.password}@{_db.host}:{_db.port}/{_db.dbname}"

pool: AsyncConnectionPool | None = None


async def start_pool():
    """Inicia el pool de conexiones a PostgreSQL."""
    global pool
    pool = AsyncConnectionPool(
        conninfo=DSN,
        min_size=_db.min_size,
        max_size=_db.max_size,
        kwargs={
            "autocommit": True,
            "application_name": _db.appname,
            "connect_timeout": int(_db.timeout_conn),
            "options": f"-c statement_timeout={int(_db.timeout_qry*1000)}",
        },
        open=False,
    )
    await pool.open()


async def stop_pool():
    """Cierra el pool de conexiones."""
    global pool
    if pool is not None:
        await pool.close()
        pool = None


@asynccontextmanager
async def get_cursor():
    """Devuelve un cursor dict_row para consultas SQL crudas."""
    assert pool is not None, "DB pool no inicializado"
    async with pool.connection() as conn:
        async with conn.cursor(row_factory=dict_row) as cur:
            yield cur
