from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class RolResponse(BaseModel):
    id: int
    nombre: str

    class Config:
        from_attributes = True


class UsuarioCreate(BaseModel):
    nombre: str
    email: EmailStr
    contrasena: str
    rol_id: int

    class Config:
        json_schema_extra = {
            "example": {
                "nombre": "Juan Pérez",
                "email": "juan@parku.edu.sv",
                "contrasena": "password123",
                "rol_id": 2,
            }
        }


class UsuarioUpdate(BaseModel):
    nombre: Optional[str] = None
    email: Optional[EmailStr] = None
    contrasena: Optional[str] = None
    estado: Optional[bool] = None
    rol_id: Optional[int] = None


class UsuarioResponse(BaseModel):
    id: int
    nombre: str
    email: str
    estado: bool
    fecha_registro: datetime
    rol_id: int
    rol: RolResponse

    class Config:
        from_attributes = True
