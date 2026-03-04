import logging
from datetime import datetime
from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.movimientos.models import Movimiento, TipoMovimiento
from app.movimientos.repository import MovimientoRepository
from app.movimientos.schemas import MovimientoDetalleResponse
from app.vehiculos.repository import VehiculoRepository
from app.parqueo.repository import ParqueoRepository

logger = logging.getLogger("parku")


class MovimientoService:
    def __init__(self, db: Session):
        self.repo = MovimientoRepository(db)
        self.vehiculo_repo = VehiculoRepository(db)
        self.parqueo_repo = ParqueoRepository(db)

    def registrar_entrada(self, placa: str, parqueo_id: int) -> Movimiento:
        # Validate vehicle exists (authorized)
        vehiculo = self.vehiculo_repo.get_by_placa(placa)
        if not vehiculo:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Vehículo no autorizado. La placa no está registrada en el sistema.",
            )

        # Validate parking lot exists
        parqueo = self.parqueo_repo.get_by_id(parqueo_id)
        if not parqueo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Parqueo no encontrado",
            )

        # RN-01: Vehicle cannot have more than one active entry simultaneously
        entrada_activa = self.repo.tiene_entrada_activa_cualquier_parqueo(vehiculo.id)
        if entrada_activa:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="El vehículo ya tiene una entrada activa. Debe registrar la salida primero.",
            )

        # RN-02: Cannot enter if no available spots
        # RN-05: Available spots calculated dynamically
        cupos_ocupados = self.repo.contar_entradas_activas(parqueo_id)
        if cupos_ocupados >= parqueo.cupos_maximos:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="No hay cupos disponibles en este parqueo",
            )

        # RN-07: fecha_hora generated server-side
        movimiento = Movimiento(
            tipo=TipoMovimiento.entrada,
            vehiculo_id=vehiculo.id,
            parqueo_id=parqueo_id,
        )

        resultado = self.repo.create(movimiento)
        logger.info(f"Entrada registrada: placa={placa}, parqueo_id={parqueo_id}")
        return resultado

    def registrar_salida(self, placa: str, parqueo_id: int) -> Movimiento:
        # Validate vehicle exists
        vehiculo = self.vehiculo_repo.get_by_placa(placa)
        if not vehiculo:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Vehículo no autorizado. La placa no está registrada en el sistema.",
            )

        # Validate parking lot exists
        parqueo = self.parqueo_repo.get_by_id(parqueo_id)
        if not parqueo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Parqueo no encontrado",
            )

        # RN-06: Vehicle must have an active entry in this parking lot
        entrada_activa = self.repo.get_entrada_activa(vehiculo.id, parqueo_id)
        if not entrada_activa:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="El vehículo no tiene una entrada activa en este parqueo",
            )

        # RN-07: fecha_hora generated server-side
        movimiento = Movimiento(
            tipo=TipoMovimiento.salida,
            vehiculo_id=vehiculo.id,
            parqueo_id=parqueo_id,
        )

        resultado = self.repo.create(movimiento)
        logger.info(f"Salida registrada: placa={placa}, parqueo_id={parqueo_id}")
        return resultado

    def obtener_activos(self, parqueo_id: Optional[int] = None) -> list[MovimientoDetalleResponse]:
        activos = self.repo.get_activos(parqueo_id)
        resultado = []
        for mov in activos:
            resultado.append(
                MovimientoDetalleResponse(
                    id=mov.id,
                    fecha_hora=mov.fecha_hora,
                    tipo=mov.tipo.value,
                    vehiculo_id=mov.vehiculo_id,
                    parqueo_id=mov.parqueo_id,
                    placa=mov.vehiculo.placa,
                    nombre_parqueo=mov.parqueo.nombre,
                )
            )
        return resultado

    def obtener_historial(
        self,
        fecha_inicio: Optional[datetime] = None,
        fecha_fin: Optional[datetime] = None,
        placa: Optional[str] = None,
        parqueo_id: Optional[int] = None,
        page: int = 1,
        size: int = 20,
    ) -> list[MovimientoDetalleResponse]:
        vehiculo_id = None
        if placa:
            vehiculo = self.vehiculo_repo.get_by_placa(placa)
            if vehiculo:
                vehiculo_id = vehiculo.id
            else:
                return []

        skip = (page - 1) * size
        movimientos = self.repo.get_historial(
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            vehiculo_id=vehiculo_id,
            parqueo_id=parqueo_id,
            skip=skip,
            limit=size,
        )

        resultado = []
        for mov in movimientos:
            resultado.append(
                MovimientoDetalleResponse(
                    id=mov.id,
                    fecha_hora=mov.fecha_hora,
                    tipo=mov.tipo.value,
                    vehiculo_id=mov.vehiculo_id,
                    parqueo_id=mov.parqueo_id,
                    placa=mov.vehiculo.placa,
                    nombre_parqueo=mov.parqueo.nombre,
                )
            )
        return resultado
