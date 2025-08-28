# app/routes/endusers.py
# This module defines end-user-related endpoints for the FastAPI application.
#

# Application imports
from fastapi import APIRouter, Depends
from app.core import jsend_success
from app.schemas.whruser import WhrUser
from datetime import datetime

# Create FastAPI router for system-related endpoints
router = APIRouter(prefix="/api/v1/users", tags=["WHR Users"])


# Dummy data for users
def get_user_list() -> list[WhrUser]:
    user_list = []
    for i in range(1, 9):
        usr = WhrUser(
            user_id=f"USUARIO{i}",
            user_email=f"usuario{i}@x.com",
            user_location=f"Ubicación usuario{i}",
            user_country=f"País usuario{i}",
            user_name=f"Nombre usuario{i}",
            supervisor_user_id=f"SUPERVI{i}",
            supervisor_name=f"Supervisor usuario{i}",
            supervisor_email=f"supervi{i}@x.com",
            user_other_info={"info": f"usuario{i}"},
            created_at=datetime.now()
        )
        user_list.append(usr)

    for i in range(10, 16):
        usr = WhrUser(
            user_id=f"USUARIO{i}",
            user_email=f"usuario{i}@x.com",
            user_location=f"Ubicación usuario{i}",
            user_country=f"País usuario{i}",
            user_name=f"Nombre usuario{i}",
            supervisor_user_id=f"SUPERVI{i}",
            supervisor_name=f"Supervisor usuario{i}",
            supervisor_email=f"supervi{i}@x.com",
            user_other_info={
                "dss_agent": True,
                "dss_info": {
                    "assignment_group": f"GTI - Desk Side - Mexico - {i}"
                }
            },
            created_at=datetime.now()
        )
        user_list.append(usr)

    return user_list


# Get all users
@router.get(
    "",
    summary="Get all users",
    dependencies=[Depends(get_user_list),]
)
async def get_all_users():
    data = get_user_list()
    return jsend_success(data=data)


# Get user by ID
@router.get(
    "/{user_id}",
    summary="Get user by ID",
    dependencies=[Depends(get_user_list),]
)
async def get_user_by_id(user_id: str):
    data = get_user_list()
    user = next((item for item in data if item.user_id == user_id), None)
    return jsend_success(data=user)


# Get dss agents
@router.get(
    "/dss/agents",
    summary="Get all dss agents",
    dependencies=[Depends(get_user_list),]
)
async def get_all_dss_agents():
    data = get_user_list()
    dss_agents = []
    for user in data:
        if (
            isinstance(user.user_other_info, dict)
            and user.user_other_info.get('dss_agent')
        ):
            dss_agents.append(user)
    return jsend_success(data=dss_agents)
