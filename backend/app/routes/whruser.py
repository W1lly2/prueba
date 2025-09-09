# app/routes/whruser.py
from fastapi import APIRouter, HTTPException, Query
from app.core.jsend import jsend_success
from app.models import whrusers

router = APIRouter(prefix="/api/v1/users", tags=["WHR Users"])

@router.get("", summary="Get all users")
async def get_all_users(
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    q: str | None = Query(None, description="buscar por nombre/email"),
    active: bool | None = Query(None),
    supervisor_id: str | None = Query(None),  # <-- texto
):
    data = await whrusers.list_users(limit, offset, q, active, supervisor_id)
    return jsend_success(data=data)

@router.get("/{user_id}", summary="Get user by ID")
async def get_user_by_id(user_id: str):  # <-- texto
    user = await whrusers.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return jsend_success(data=user)

@router.get("/dss/agents", summary="Get all DSS agents")
async def get_all_dss_agents():
    data = await whrusers.list_users(limit=200)
    dss_agents = [
        u for u in data
        if isinstance(u.get("user_other_info"), dict) and u["user_other_info"].get("dss_agent")
    ]
    return jsend_success(data=dss_agents)
