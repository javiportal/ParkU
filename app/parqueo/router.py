from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies import get_db, get_current_user, require_role
from app.usuarios.models import Usuario
from app.parqueo.schemas import ParqueoCreate, ParqueoUpdate, ParqueoResponse, DisponibilidadResponse
from app.parqueo.service import ParqueoService

router = APIRouter(prefix="/api/parqueos", tags=["Parqueo"])

admin_only = require_role(["administrador"])


@router.post(
    "",
    response_model=ParqueoResponse,
    status_code=201,
    summary="Crear parqueo",
    description="Crea un nuevo parqueo. Solo administradores.",
)
def crear_parqueo(
    data: ParqueoCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(admin_only),
):
    service = ParqueoService(db)
    return service.crear_parqueo(data)


@router.get(
    "",
    response_model=list[ParqueoResponse],
    summary="Listar parqueos",
    description="Obtiene la lista de parqueos. Todos los usuarios autenticados.",
)
def listar_parqueos(
    page: int = 1,
    size: int = 20,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    service = ParqueoService(db)
    return service.listar_parqueos(page=page, size=size)


@router.get(
    "/{parqueo_id}",
    response_model=ParqueoResponse,
    summary="Obtener parqueo",
    description="Obtiene los detalles de un parqueo. Todos los usuarios autenticados.",
)
def obtener_parqueo(
    parqueo_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    service = ParqueoService(db)
    return service.obtener_parqueo(parqueo_id)


@router.put(
    "/{parqueo_id}",
    response_model=ParqueoResponse,
    summary="Actualizar parqueo",
    description="Actualiza los datos de un parqueo. Solo administradores.",
)
def actualizar_parqueo(
    parqueo_id: int,
    data: ParqueoUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(admin_only),
):
    service = ParqueoService(db)
    return service.actualizar_parqueo(parqueo_id, data)


@router.get(
    "/{parqueo_id}/disponibilidad",
    response_model=DisponibilidadResponse,
    summary="Consultar disponibilidad",
    description="Obtiene los cupos disponibles en tiempo real. Todos los usuarios autenticados.",
)
def obtener_disponibilidad(
    parqueo_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    service = ParqueoService(db)
    return service.obtener_disponibilidad(parqueo_id)
