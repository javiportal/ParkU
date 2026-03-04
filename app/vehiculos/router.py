from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies import get_db, require_role
from app.usuarios.models import Usuario
from app.vehiculos.schemas import VehiculoCreate, VehiculoUpdate, VehiculoResponse
from app.vehiculos.service import VehiculoService

router = APIRouter(prefix="/api/vehiculos", tags=["Vehiculos"])

admin_only = require_role(["administrador"])
admin_vigilante = require_role(["administrador", "vigilante"])


@router.post(
    "",
    response_model=VehiculoResponse,
    status_code=201,
    summary="Registrar vehículo",
    description="Registra un vehículo autorizado. Solo administradores.",
)
def crear_vehiculo(
    data: VehiculoCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(admin_only),
):
    service = VehiculoService(db)
    return service.crear_vehiculo(data)


@router.get(
    "/buscar",
    response_model=VehiculoResponse,
    summary="Buscar vehículo por placa",
    description="Busca un vehículo por su placa. Admin y Vigilante.",
)
def buscar_por_placa(
    placa: str,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(admin_vigilante),
):
    service = VehiculoService(db)
    return service.buscar_por_placa(placa)


@router.get(
    "",
    response_model=list[VehiculoResponse],
    summary="Listar vehículos",
    description="Obtiene la lista de vehículos registrados. Admin y Vigilante.",
)
def listar_vehiculos(
    page: int = 1,
    size: int = 20,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(admin_vigilante),
):
    service = VehiculoService(db)
    return service.listar_vehiculos(page=page, size=size)


@router.get(
    "/{vehiculo_id}",
    response_model=VehiculoResponse,
    summary="Obtener vehículo por ID",
    description="Obtiene los detalles de un vehículo. Admin y Vigilante.",
)
def obtener_vehiculo(
    vehiculo_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(admin_vigilante),
):
    service = VehiculoService(db)
    return service.obtener_vehiculo(vehiculo_id)


@router.put(
    "/{vehiculo_id}",
    response_model=VehiculoResponse,
    summary="Actualizar vehículo",
    description="Actualiza los datos de un vehículo. Solo administradores.",
)
def actualizar_vehiculo(
    vehiculo_id: int,
    data: VehiculoUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(admin_only),
):
    service = VehiculoService(db)
    return service.actualizar_vehiculo(vehiculo_id, data)


@router.delete(
    "/{vehiculo_id}",
    status_code=204,
    summary="Eliminar vehículo",
    description="Elimina un vehículo del sistema. Solo administradores.",
)
def eliminar_vehiculo(
    vehiculo_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(admin_only),
):
    service = VehiculoService(db)
    service.eliminar_vehiculo(vehiculo_id)
