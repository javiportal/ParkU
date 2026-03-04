from datetime import datetime

from pydantic import BaseModel


class MovimientoEntradaRequest(BaseModel):
    placa: str
    parqueo_id: int

    class Config:
        json_schema_extra = {
            "example": {
                "placa": "P-123-456",
                "parqueo_id": 1,
            }
        }


class MovimientoSalidaRequest(BaseModel):
    placa: str
    parqueo_id: int


class MovimientoResponse(BaseModel):
    id: int
    fecha_hora: datetime
    tipo: str
    vehiculo_id: int
    parqueo_id: int

    class Config:
        from_attributes = True


class MovimientoDetalleResponse(BaseModel):
    id: int
    fecha_hora: datetime
    tipo: str
    vehiculo_id: int
    parqueo_id: int
    placa: str
    nombre_parqueo: str
