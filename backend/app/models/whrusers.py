# app/models/whrusers.py
from typing import List, Optional
from app.core.db import get_cursor

SELECT_BASE = """
select
  user_id,
  user_email,
  user_location,
  user_country,
  user_active,
  user_name,
  supervisor_user_id,
  supervisor_name,
  supervisor_email,
  user_other_info,
  created_at,
  updated_at
from whr_user
"""

async def list_users(
    limit: int = 50,
    offset: int = 0,
    q: str | None = None,               # búsqueda por nombre/email
    active: Optional[bool] = None,      # filtrar por activo
    supervisor_id: Optional[str] = None # filtrar por supervisor (texto)
) -> List[dict]:
    where = []
    params: list = []

    if q:
        where.append("(user_name ilike %s or user_email ilike %s)")
        like = f"%{q}%"
        params += [like, like]

    if active is not None:
        where.append("user_active = %s")
        params.append(active)

    if supervisor_id is not None:
        where.append("supervisor_user_id = %s")
        params.append(supervisor_id)

    where_sql = f" where {' and '.join(where)}" if where else ""
    params += [limit, offset]

    sql = SELECT_BASE + where_sql + " order by created_at desc limit %s offset %s"
    async with get_cursor() as cur:
        await cur.execute(sql, tuple(params))
        return await cur.fetchall()

async def get_user(user_id: str) -> Optional[dict]:
    sql = SELECT_BASE + " where user_id = %s"
    async with get_cursor() as cur:
        await cur.execute(sql, (user_id,))
        return await cur.fetchone()

async def get_user_by_email(email: str) -> Optional[dict]:
    sql = SELECT_BASE + " where user_email = %s"
    async with get_cursor() as cur:
        await cur.execute(sql, (email,))
        return await cur.fetchone()
