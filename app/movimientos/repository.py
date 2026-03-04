from datetime import datetime
from typing import Optional

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.movimientos.models import Movimiento, TipoMovimiento


class MovimientoRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, movimiento_id: int) -> Movimiento | None:
        return self.db.query(Movimiento).filter(Movimiento.id == movimiento_id).first()

    def create(self, movimiento: Movimiento) -> Movimiento:
        self.db.add(movimiento)
        self.db.commit()
        self.db.refresh(movimiento)
        return movimiento

    def get_entrada_activa(self, vehiculo_id: int, parqueo_id: int) -> Movimiento | None:
        """Finds an active entry (entrada without a subsequent salida) for a vehicle in a parking lot."""
        from sqlalchemy import and_

        ultima_entrada = (
            self.db.query(Movimiento)
            .filter(
                Movimiento.vehiculo_id == vehiculo_id,
                Movimiento.parqueo_id == parqueo_id,
                Movimiento.tipo == TipoMovimiento.entrada,
            )
            .order_by(Movimiento.fecha_hora.desc())
            .first()
        )

        if not ultima_entrada:
            return None

        salida_posterior = (
            self.db.query(Movimiento)
            .filter(
                Movimiento.vehiculo_id == vehiculo_id,
                Movimiento.parqueo_id == parqueo_id,
                Movimiento.tipo == TipoMovimiento.salida,
                Movimiento.fecha_hora > ultima_entrada.fecha_hora,
            )
            .first()
        )

        if salida_posterior:
            return None

        return ultima_entrada

    def tiene_entrada_activa_cualquier_parqueo(self, vehiculo_id: int) -> Movimiento | None:
        """Check if vehicle has an active entry in ANY parking lot (RN-01)."""
        from sqlalchemy import and_

        entradas = (
            self.db.query(Movimiento)
            .filter(
                Movimiento.vehiculo_id == vehiculo_id,
                Movimiento.tipo == TipoMovimiento.entrada,
            )
            .order_by(Movimiento.fecha_hora.desc())
            .all()
        )

        for entrada in entradas:
            salida_posterior = (
                self.db.query(Movimiento)
                .filter(
                    Movimiento.vehiculo_id == vehiculo_id,
                    Movimiento.parqueo_id == entrada.parqueo_id,
                    Movimiento.tipo == TipoMovimiento.salida,
                    Movimiento.fecha_hora > entrada.fecha_hora,
                )
                .first()
            )
            if not salida_posterior:
                return entrada

        return None

    def contar_entradas_activas(self, parqueo_id: int) -> int:
        """Count active entries in a parking lot (RN-05: dynamic availability)."""
        entradas = (
            self.db.query(Movimiento)
            .filter(
                Movimiento.parqueo_id == parqueo_id,
                Movimiento.tipo == TipoMovimiento.entrada,
            )
            .all()
        )

        count = 0
        for entrada in entradas:
            salida = (
                self.db.query(Movimiento)
                .filter(
                    Movimiento.vehiculo_id == entrada.vehiculo_id,
                    Movimiento.parqueo_id == parqueo_id,
                    Movimiento.tipo == TipoMovimiento.salida,
                    Movimiento.fecha_hora > entrada.fecha_hora,
                )
                .first()
            )
            if not salida:
                count += 1

        return count

    def get_activos(self, parqueo_id: Optional[int] = None) -> list[Movimiento]:
        """Get all vehicles currently inside (active entries without exit)."""
        query = self.db.query(Movimiento).filter(
            Movimiento.tipo == TipoMovimiento.entrada
        )

        if parqueo_id:
            query = query.filter(Movimiento.parqueo_id == parqueo_id)

        entradas = query.order_by(Movimiento.fecha_hora.desc()).all()
        activos = []

        seen_vehicles = set()
        for entrada in entradas:
            if entrada.vehiculo_id in seen_vehicles:
                continue

            salida = (
                self.db.query(Movimiento)
                .filter(
                    Movimiento.vehiculo_id == entrada.vehiculo_id,
                    Movimiento.parqueo_id == entrada.parqueo_id,
                    Movimiento.tipo == TipoMovimiento.salida,
                    Movimiento.fecha_hora > entrada.fecha_hora,
                )
                .first()
            )
            if not salida:
                activos.append(entrada)
                seen_vehicles.add(entrada.vehiculo_id)

        return activos

    def get_historial(
        self,
        fecha_inicio: Optional[datetime] = None,
        fecha_fin: Optional[datetime] = None,
        vehiculo_id: Optional[int] = None,
        parqueo_id: Optional[int] = None,
        skip: int = 0,
        limit: int = 20,
    ) -> list[Movimiento]:
        query = self.db.query(Movimiento)

        if fecha_inicio:
            query = query.filter(Movimiento.fecha_hora >= fecha_inicio)
        if fecha_fin:
            query = query.filter(Movimiento.fecha_hora <= fecha_fin)
        if vehiculo_id:
            query = query.filter(Movimiento.vehiculo_id == vehiculo_id)
        if parqueo_id:
            query = query.filter(Movimiento.parqueo_id == parqueo_id)

        return query.order_by(Movimiento.fecha_hora.desc()).offset(skip).limit(limit).all()
