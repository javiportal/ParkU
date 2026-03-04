from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies import get_db, require_role
from app.usuarios.models import Usuario
from app.usuarios.schemas import UsuarioCreate, UsuarioUpdate, UsuarioResponse
from app.usuarios.service import UsuarioService

router = APIRouter(prefix="/api/usuarios", tags=["Usuarios"])

admin_only = require_role(["administrador"])


@router.post(
    "",
    response_model=UsuarioResponse,
    status_code=201,
    summary="Crear usuario",
    description="Crea un nuevo usuario con un rol asignado. Solo administradores.",
)
def crear_usuario(
    data: UsuarioCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(admin_only),
):
    service = UsuarioService(db)
    return service.crear_usuario(data)


@router.get(
    "",
    response_model=list[UsuarioResponse],
    summary="Listar usuarios",
    description="Obtiene la lista de todos los usuarios. Solo administradores.",
)
def listar_usuarios(
    page: int = 1,
    size: int = 20,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(admin_only),
):
    service = UsuarioService(db)
    return service.listar_usuarios(page=page, size=size)


@router.get(
    "/{usuario_id}",
    response_model=UsuarioResponse,
    summary="Obtener usuario por ID",
    description="Obtiene los detalles de un usuario específico. Solo administradores.",
)
def obtener_usuario(
    usuario_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(admin_only),
):
    service = UsuarioService(db)
    return service.obtener_usuario(usuario_id)


@router.put(
    "/{usuario_id}",
    response_model=UsuarioResponse,
    summary="Actualizar usuario",
    description="Actualiza los datos de un usuario. Solo administradores.",
)
def actualizar_usuario(
    usuario_id: int,
    data: UsuarioUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(admin_only),
):
    service = UsuarioService(db)
    return service.actualizar_usuario(usuario_id, data)


@router.delete(
    "/{usuario_id}",
    response_model=UsuarioResponse,
    summary="Desactivar usuario",
    description="Desactiva un usuario (soft delete). Solo administradores.",
)
def desactivar_usuario(
    usuario_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(admin_only),
):
    service = UsuarioService(db)
    return service.desactivar_usuario(usuario_id)
