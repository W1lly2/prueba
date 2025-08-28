# app/main.py

# Configuration imports
from app.core.config import AppSettings
# Logging imports
from loguru import logger
# FastAPI imports
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
# Routers imports
from app.routes.system import router as system_router
from app.routes.whruser import router as whrusers_router
from app.routes.whrasset import router as whrassets_router


# FastAPI lifespan events
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup lifespan event handler
    logger.info(f"Starting up {app.title} v{app.version} application...")

    # Yield control back to FastAPI
    yield

    # Shutdown lifespan event handler
    logger.info(f"Shutting down {app.title} v{app.version} application...")


# Create FastAPI app
app = FastAPI(
    lifespan=lifespan,
    title=AppSettings.name,
    version=AppSettings.version,
    description=AppSettings.description,
    default_response_class=JSONResponse
)

# CORS middleware
app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,  # Allow cookies and authorization headers
        allow_methods=["*"],     # Allow all HTTP methods(GET, POST, etc.)
        allow_headers=["*"],     # Allow all headers
    )


# Include routers
app.include_router(system_router)
app.include_router(whrusers_router)
app.include_router(whrassets_router)
