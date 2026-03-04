from sqlalchemy.orm import Session

from app.usuarios.models import Rol, Usuario


class RolRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, rol_id: int) -> Rol | None:
        return self.db.query(Rol).filter(Rol.id == rol_id).first()

    def get_by_nombre(self, nombre: str) -> Rol | None:
        return self.db.query(Rol).filter(Rol.nombre == nombre).first()

    def get_all(self) -> list[Rol]:
        return self.db.query(Rol).all()

    def create(self, nombre: str) -> Rol:
        rol = Rol(nombre=nombre)
        self.db.add(rol)
        self.db.commit()
        self.db.refresh(rol)
        return rol


class UsuarioRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, usuario_id: int) -> Usuario | None:
        return self.db.query(Usuario).filter(Usuario.id == usuario_id).first()

    def get_by_email(self, email: str) -> Usuario | None:
        return self.db.query(Usuario).filter(Usuario.email == email).first()

    def get_all(self, skip: int = 0, limit: int = 20) -> list[Usuario]:
        return self.db.query(Usuario).offset(skip).limit(limit).all()

    def create(self, usuario: Usuario) -> Usuario:
        self.db.add(usuario)
        self.db.commit()
        self.db.refresh(usuario)
        return usuario

    def update(self, usuario: Usuario) -> Usuario:
        self.db.commit()
        self.db.refresh(usuario)
        return usuario

    def count(self) -> int:
        return self.db.query(Usuario).count()
