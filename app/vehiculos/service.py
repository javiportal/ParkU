from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.vehiculos.models import Vehiculo
from app.vehiculos.repository import VehiculoRepository
from app.vehiculos.schemas import VehiculoCreate, VehiculoUpdate


class VehiculoService:
    def __init__(self, db: Session):
        self.repo = VehiculoRepository(db)

    def crear_vehiculo(self, data: VehiculoCreate) -> Vehiculo:
        # RN-08: No placas duplicadas
        if self.repo.get_by_placa(data.placa):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="La placa ya está registrada",
            )

        vehiculo = Vehiculo(
            placa=data.placa,
            marca=data.marca,
            modelo=data.modelo,
            color=data.color,
            usuario_id=data.usuario_id,
        )
        return self.repo.create(vehiculo)

    def obtener_vehiculo(self, vehiculo_id: int) -> Vehiculo:
        vehiculo = self.repo.get_by_id(vehiculo_id)
        if not vehiculo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Vehículo no encontrado",
            )
        return vehiculo

    def listar_vehiculos(self, page: int = 1, size: int = 20) -> list[Vehiculo]:
        skip = (page - 1) * size
        return self.repo.get_all(skip=skip, limit=size)

    def buscar_por_placa(self, placa: str) -> Vehiculo:
        vehiculo = self.repo.get_by_placa(placa)
        if not vehiculo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Vehículo no encontrado",
            )
        return vehiculo

    def actualizar_vehiculo(self, vehiculo_id: int, data: VehiculoUpdate) -> Vehiculo:
        vehiculo = self.obtener_vehiculo(vehiculo_id)

        if data.placa is not None:
            existing = self.repo.get_by_placa(data.placa)
            if existing and existing.id != vehiculo_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="La placa ya está registrada",
                )
            vehiculo.placa = data.placa
        if data.marca is not None:
            vehiculo.marca = data.marca
        if data.modelo is not None:
            vehiculo.modelo = data.modelo
        if data.color is not None:
            vehiculo.color = data.color
        if data.usuario_id is not None:
            vehiculo.usuario_id = data.usuario_id

        return self.repo.update(vehiculo)

    def eliminar_vehiculo(self, vehiculo_id: int) -> None:
        vehiculo = self.obtener_vehiculo(vehiculo_id)
        self.repo.delete(vehiculo)
