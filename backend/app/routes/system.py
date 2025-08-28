# app/routes/system.py
# This module defines system-related endpoints for the FastAPI application.
#

# Application imports
from fastapi import APIRouter
from app.core import AppSettings
from app.core import jsend_success

# Create FastAPI router for system-related endpoints
router = APIRouter()


# Endpoint for health check
@router.get("/")
async def root():
    data = {
        "app_name": AppSettings.name,
        "app_version": AppSettings.version,
        "app_description": AppSettings.description
    }
    return jsend_success(data=data)
