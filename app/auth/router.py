from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.auth.schemas import LoginRequest, TokenResponse
from app.auth.service import authenticate_user
from app.auth.jwt_handler import create_access_token

router = APIRouter(prefix="/api/auth", tags=["Auth"])


@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Iniciar sesión",
    description="Autenticación con email y contraseña. Retorna un token JWT.",
)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    usuario = authenticate_user(db, request.email, request.contrasena)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas",
        )

    token = create_access_token(
        data={"sub": str(usuario.id), "rol": usuario.rol.nombre}
    )
    return TokenResponse(access_token=token)
