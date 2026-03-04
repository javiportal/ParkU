import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from app.database import engine, SessionLocal
from app.middleware.request_id import RequestIDMiddleware
from app.middleware.logging_middleware import LoggingMiddleware
from app.seed import seed

from app.auth.router import router as auth_router
from app.usuarios.router import router as usuarios_router
from app.vehiculos.router import router as vehiculos_router
from app.parqueo.router import router as parqueo_router
from app.movimientos.router import router as movimientos_router

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("parku")

app = FastAPI(
    title="ParkU API",
    description="Sistema de Gestión de Parqueo Universitario - ESEN",
    version="1.0.0",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Middleware (order matters: request_id first so logging can use it)
app.add_middleware(LoggingMiddleware)
app.add_middleware(RequestIDMiddleware)

@app.on_event("startup")
def on_startup():
    seed()


# Routers
app.include_router(auth_router)
app.include_router(usuarios_router)
app.include_router(vehiculos_router)
app.include_router(parqueo_router)
app.include_router(movimientos_router)


@app.get("/health", tags=["Health"], summary="Estado del sistema")
def health():
    return {"status": "ok"}


@app.get("/ready", tags=["Health"], summary="Verificar conexión a BD")
def ready():
    try:
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        db.close()
        return {"status": "ready", "database": "connected"}
    except Exception as e:
        return {"status": "not_ready", "database": str(e)}
