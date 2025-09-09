# app/routes/whrasset.py
from fastapi import APIRouter, HTTPException, Query
from app.core.jsend import jsend_success
import app.models.whrasset as whrassets  # SQL plano, sin ORM

router = APIRouter(prefix="/api/v1/assets", tags=["WHR Assets"])

# GET /api/v1/assets?asset_serial_number=...   (o lista/búsqueda con q)
@router.get("", summary="List/search or get by serial (query)")
async def get_assets(
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    q: str | None = Query(None, description="buscar por serial/tag/descripcion"),
    asset_serial_number: str | None = Query(None, description="búsqueda exacta por serial"),
):
    if asset_serial_number:
        asset = await whrassets.get_by_serial(asset_serial_number)
        if not asset:
            raise HTTPException(status_code=404, detail="Asset no encontrado")
        # >>> Clave: tu front espera un ARRAY como en el listado
        return jsend_success(data=[asset])

    data = await whrassets.list_assets(limit, offset, q)
    return jsend_success(data=data)

# GET /api/v1/assets/{asset_serial_number}  (devuelve un objeto)
@router.get("/{asset_serial_number}", summary="Get by serial (path)")
async def get_asset_by_serial_number(asset_serial_number: str):
    asset = await whrassets.get_by_serial(asset_serial_number)
    if not asset:
        raise HTTPException(status_code=404, detail="Asset no encontrado")
    return jsend_success(data=asset)
