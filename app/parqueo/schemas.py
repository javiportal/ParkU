from typing import Optional

from pydantic import BaseModel


class ParqueoCreate(BaseModel):
    nombre: str
    cupos_maximos: int

    class Config:
        json_schema_extra = {
            "example": {
                "nombre": "Parqueo Norte",
                "cupos_maximos": 100,
            }
        }


class ParqueoUpdate(BaseModel):
    nombre: Optional[str] = None
    cupos_maximos: Optional[int] = None


class ParqueoResponse(BaseModel):
    id: int
    nombre: str
    cupos_maximos: int

    class Config:
        from_attributes = True


class DisponibilidadResponse(BaseModel):
    parqueo_id: int
    nombre: str
    cupos_maximos: int
    cupos_ocupados: int
    cupos_disponibles: int
