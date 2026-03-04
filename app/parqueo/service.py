from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.parqueo.models import Parqueo
from app.parqueo.repository import ParqueoRepository
from app.parqueo.schemas import ParqueoCreate, ParqueoUpdate, DisponibilidadResponse
from app.movimientos.repository import MovimientoRepository


class ParqueoService:
    def __init__(self, db: Session):
        self.repo = ParqueoRepository(db)
        self.mov_repo = MovimientoRepository(db)

    def crear_parqueo(self, data: ParqueoCreate) -> Parqueo:
        if data.cupos_maximos <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Los cupos máximos deben ser mayores a 0",
            )

        parqueo = Parqueo(
            nombre=data.nombre,
            cupos_maximos=data.cupos_maximos,
        )
        return self.repo.create(parqueo)

    def obtener_parqueo(self, parqueo_id: int) -> Parqueo:
        parqueo = self.repo.get_by_id(parqueo_id)
        if not parqueo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Parqueo no encontrado",
            )
        return parqueo

    def listar_parqueos(self, page: int = 1, size: int = 20) -> list[Parqueo]:
        skip = (page - 1) * size
        return self.repo.get_all(skip=skip, limit=size)

    def actualizar_parqueo(self, parqueo_id: int, data: ParqueoUpdate) -> Parqueo:
        parqueo = self.obtener_parqueo(parqueo_id)

        if data.nombre is not None:
            parqueo.nombre = data.nombre
        if data.cupos_maximos is not None:
            if data.cupos_maximos <= 0:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Los cupos máximos deben ser mayores a 0",
                )
            parqueo.cupos_maximos = data.cupos_maximos

        return self.repo.update(parqueo)

    def obtener_disponibilidad(self, parqueo_id: int) -> DisponibilidadResponse:
        """RN-05: cupos_disponibles calculated dynamically."""
        parqueo = self.obtener_parqueo(parqueo_id)
        cupos_ocupados = self.mov_repo.contar_entradas_activas(parqueo_id)
        cupos_disponibles = parqueo.cupos_maximos - cupos_ocupados

        return DisponibilidadResponse(
            parqueo_id=parqueo.id,
            nombre=parqueo.nombre,
            cupos_maximos=parqueo.cupos_maximos,
            cupos_ocupados=cupos_ocupados,
            cupos_disponibles=max(0, cupos_disponibles),
        )
