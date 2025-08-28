# app/routes/whrasset.py
# This module defines asset-related endpoints for the FastAPI application.
#

# Application imports
from fastapi import APIRouter, Depends
from app.core import jsend_success
from app.schemas.whrasset import WhrAsset
from datetime import datetime
from uuid import uuid4

# Create FastAPI router for system-related endpoints
router = APIRouter(prefix="/api/v1/assets", tags=["WHR Assets"])


# Dummy data for assets
def get_assets_list() -> list[WhrAsset]:
    asset_list = []
    for i in range(1, 9):
        asset = WhrAsset(
            asset_id=str(uuid4()),
            contract_id=f"CONTRACT{i}",
            contract_start_date=datetime.now(),
            contract_maturity_date=datetime.now(),
            asset_serial_number=f"SN{i}",
            asset_tag=f"TAG{i}",
            asset_description=f"Descripción del activo {i}",
            asset_type=f"Tipo {i}",
            asset_status=f"Estado {i}",
            asset_other_info={"info": f"activo{i}"},
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        asset_list.append(asset)
    return asset_list


# Get all assets
@router.get(
    "",
    summary="Get all assets",
    dependencies=[Depends(get_assets_list),]
)
async def get_assets():
    data = get_assets_list()
    return jsend_success(data=data)


# Get asset by serial num
@router.get(
    "/{asset_serial_number}",
    summary="Get asset by serial number",
    dependencies=[Depends(get_assets_list),]
)
async def get_asset_by_serial_number(asset_serial_number: str):
    data = get_assets_list()
    asset = next(
        (
            item for item in data
            if item.asset_serial_number == asset_serial_number
        ),
        None
    )
    return jsend_success(data=asset)
