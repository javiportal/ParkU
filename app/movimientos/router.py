from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.dependencies import get_db, require_role
from app.usuarios.models import Usuario
from app.movimientos.schemas import (
    MovimientoEntradaRequest,
    MovimientoSalidaRequest,
    MovimientoResponse,
    MovimientoDetalleResponse,
)
from app.movimientos.service import MovimientoService

router = APIRouter(prefix="/api/movimientos", tags=["Movimientos"])

vigilante_only = require_role(["vigilante"])
admin_only = require_role(["administrador"])
admin_vigilante = require_role(["administrador", "vigilante"])


@router.post(
    "/entrada",
    response_model=MovimientoResponse,
    status_code=201,
    summary="Registrar entrada",
    description="Registra la entrada de un vehículo a un parqueo. Solo vigilantes.",
)
def registrar_entrada(
    data: MovimientoEntradaRequest,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(vigilante_only),
):
    service = MovimientoService(db)
    return service.registrar_entrada(data.placa, data.parqueo_id)


@router.post(
    "/salida",
    response_model=MovimientoResponse,
    status_code=201,
    summary="Registrar salida",
    description="Registra la salida de un vehículo de un parqueo. Solo vigilantes.",
)
def registrar_salida(
    data: MovimientoSalidaRequest,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(vigilante_only),
):
    service = MovimientoService(db)
    return service.registrar_salida(data.placa, data.parqueo_id)


@router.get(
    "/activos",
    response_model=list[MovimientoDetalleResponse],
    summary="Vehículos activos",
    description="Lista los vehículos actualmente dentro del parqueo. Admin y Vigilante.",
)
def obtener_activos(
    parqueo_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(admin_vigilante),
):
    service = MovimientoService(db)
    return service.obtener_activos(parqueo_id)


@router.get(
    "/historial",
    response_model=list[MovimientoDetalleResponse],
    summary="Historial de movimientos",
    description="Obtiene el historial de movimientos con filtros. Solo administradores.",
)
def obtener_historial(
    fecha_inicio: Optional[datetime] = Query(None),
    fecha_fin: Optional[datetime] = Query(None),
    placa: Optional[str] = Query(None),
    parqueo_id: Optional[int] = Query(None),
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(admin_only),
):
    service = MovimientoService(db)
    return service.obtener_historial(
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin,
        placa=placa,
        parqueo_id=parqueo_id,
        page=page,
        size=size,
    )
