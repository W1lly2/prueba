# app/models/whrassets.py
from typing import List, Optional
from app.core.db import get_cursor

SELECT_BASE = """
select
  asset_id,
  contract_id,
  contract_start_date,
  contract_maturity_date,
  asset_serial_number,
  asset_tag,
  asset_description,
  asset_type,
  asset_status,
  asset_other_info,
  created_at,
  updated_at
from whr_asset
"""

async def list_assets(
    limit: int = 50,
    offset: int = 0,
    q: str | None = None  # busca por serial/tag/descripcion
) -> List[dict]:
    where, params = "", []
    if q:
        where = " where asset_serial_number ilike %s or asset_tag ilike %s or asset_description ilike %s "
        like = f"%{q}%"
        params += [like, like, like]
    params += [limit, offset]
    sql = SELECT_BASE + where + " order by created_at desc limit %s offset %s"
    async with get_cursor() as cur:
        await cur.execute(sql, tuple(params))
        return await cur.fetchall()

async def get_by_serial(asset_serial_number: str) -> Optional[dict]:
    sql = SELECT_BASE + " where asset_serial_number = %s"
    async with get_cursor() as cur:
        await cur.execute(sql, (asset_serial_number,))
        return await cur.fetchone()

# (Opcional) por id si lo necesitas más adelante
async def get_by_id(asset_id: str) -> Optional[dict]:
    sql = SELECT_BASE + " where asset_id = %s"
    async with get_cursor() as cur:
        await cur.execute(sql, (asset_id,))
        return await cur.fetchone()
