# app/schemas/whrasset.py
# Import pydantics
from pydantic.main import BaseModel
from typing import Optional, Any
from datetime import datetime


# EndUser schema
class WhrAsset(BaseModel):
    asset_id: str
    contract_id: Optional[str] = None
    contract_start_date: Optional[datetime] = None
    contract_maturity_date: Optional[datetime] = None
    asset_serial_number: str
    asset_tag: Optional[str] = None
    asset_description: str
    asset_type: Optional[str] = None
    asset_status: Optional[str] = None
    asset_other_info: Optional[dict[str, Any]] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
