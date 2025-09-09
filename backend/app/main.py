# app/main.py

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from loguru import logger

# Config & DB
from app.core.config import AppSettings
from app.core.db import start_pool, stop_pool, get_cursor

# Routers
from app.routes.system import router as system_router
from app.routes.whruser import router as whrusers_router
from app.routes.whrasset import router as whrassets_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info(f"Starting up {app.title} v{app.version}...")
    await start_pool()  # abrir pool de conexión a DB
    try:
        yield
    finally:
        # Shutdown
        await stop_pool()  # cerrar pool de conexión a DB
        logger.info(f"Shutting down {app.title} v{app.version}...")


app = FastAPI(
    title=AppSettings.name,
    version=AppSettings.version,
    description=AppSettings.description,
    default_response_class=JSONResponse,
    lifespan=lifespan,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(system_router)
app.include_router(whrusers_router)
app.include_router(whrassets_router)

# Raíz y healthchecks
@app.get("/", tags=["System"])
async def root():
    return {"ok": True, "name": AppSettings.name, "version": AppSettings.version}

@app.get("/health/db", tags=["System"])
async def db_health():
    async with get_cursor() as cur:
        await cur.execute("select 1 as ok")
        return await cur.fetchone()
