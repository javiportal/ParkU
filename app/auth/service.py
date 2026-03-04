from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.usuarios.repository import UsuarioRepository
from app.usuarios.models import Usuario

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def authenticate_user(db: Session, email: str, contrasena: str) -> Usuario | None:
    repo = UsuarioRepository(db)
    usuario = repo.get_by_email(email)
    if not usuario:
        return None
    if not usuario.estado:
        return None
    if not verify_password(contrasena, usuario.contrasena):
        return None
    return usuario
