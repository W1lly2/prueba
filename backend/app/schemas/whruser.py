# app/schemas/whruser.py
# Import pydantics
from pydantic.main import BaseModel
from typing import Optional, Any
from datetime import datetime


# EndUser schema
class WhrUser(BaseModel):
    user_id: str
    user_email: str
    user_location: Optional[str] = None
    user_country: Optional[str] = None
    user_active: bool = True
    user_name: Optional[str] = None
    supervisor_user_id: Optional[str] = None
    supervisor_name: Optional[str] = None
    supervisor_email: Optional[str] = None
    user_other_info: Optional[dict[str, Any]] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
