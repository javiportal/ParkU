from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.auth.service import hash_password
from app.usuarios.models import Usuario
from app.usuarios.repository import UsuarioRepository, RolRepository
from app.usuarios.schemas import UsuarioCreate, UsuarioUpdate


class UsuarioService:
    def __init__(self, db: Session):
        self.repo = UsuarioRepository(db)
        self.rol_repo = RolRepository(db)

    def crear_usuario(self, data: UsuarioCreate) -> Usuario:
        if self.repo.get_by_email(data.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El email ya está registrado",
            )

        rol = self.rol_repo.get_by_id(data.rol_id)
        if not rol:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Rol no encontrado",
            )

        usuario = Usuario(
            nombre=data.nombre,
            email=data.email,
            contrasena=hash_password(data.contrasena),
            rol_id=data.rol_id,
        )
        return self.repo.create(usuario)

    def obtener_usuario(self, usuario_id: int) -> Usuario:
        usuario = self.repo.get_by_id(usuario_id)
        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado",
            )
        return usuario

    def listar_usuarios(self, page: int = 1, size: int = 20) -> list[Usuario]:
        skip = (page - 1) * size
        return self.repo.get_all(skip=skip, limit=size)

    def actualizar_usuario(self, usuario_id: int, data: UsuarioUpdate) -> Usuario:
        usuario = self.obtener_usuario(usuario_id)

        if data.nombre is not None:
            usuario.nombre = data.nombre
        if data.email is not None:
            existing = self.repo.get_by_email(data.email)
            if existing and existing.id != usuario_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="El email ya está registrado",
                )
            usuario.email = data.email
        if data.contrasena is not None:
            usuario.contrasena = hash_password(data.contrasena)
        if data.estado is not None:
            usuario.estado = data.estado
        if data.rol_id is not None:
            rol = self.rol_repo.get_by_id(data.rol_id)
            if not rol:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Rol no encontrado",
                )
            usuario.rol_id = data.rol_id

        return self.repo.update(usuario)

    def desactivar_usuario(self, usuario_id: int) -> Usuario:
        usuario = self.obtener_usuario(usuario_id)
        usuario.estado = False
        return self.repo.update(usuario)
