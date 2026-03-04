from typing import Optional

from pydantic import BaseModel


class VehiculoCreate(BaseModel):
    placa: str
    marca: str
    modelo: str
    color: str
    usuario_id: int

    class Config:
        json_schema_extra = {
            "example": {
                "placa": "P-123-456",
                "marca": "Toyota",
                "modelo": "Corolla",
                "color": "Blanco",
                "usuario_id": 1,
            }
        }


class VehiculoUpdate(BaseModel):
    placa: Optional[str] = None
    marca: Optional[str] = None
    modelo: Optional[str] = None
    color: Optional[str] = None
    usuario_id: Optional[int] = None


class VehiculoResponse(BaseModel):
    id: int
    placa: str
    marca: str
    modelo: str
    color: str
    usuario_id: int

    class Config:
        from_attributes = True
