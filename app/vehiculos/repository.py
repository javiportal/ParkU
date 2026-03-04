from sqlalchemy.orm import Session

from app.vehiculos.models import Vehiculo


class VehiculoRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, vehiculo_id: int) -> Vehiculo | None:
        return self.db.query(Vehiculo).filter(Vehiculo.id == vehiculo_id).first()

    def get_by_placa(self, placa: str) -> Vehiculo | None:
        return self.db.query(Vehiculo).filter(Vehiculo.placa == placa).first()

    def get_all(self, skip: int = 0, limit: int = 20) -> list[Vehiculo]:
        return self.db.query(Vehiculo).offset(skip).limit(limit).all()

    def create(self, vehiculo: Vehiculo) -> Vehiculo:
        self.db.add(vehiculo)
        self.db.commit()
        self.db.refresh(vehiculo)
        return vehiculo

    def update(self, vehiculo: Vehiculo) -> Vehiculo:
        self.db.commit()
        self.db.refresh(vehiculo)
        return vehiculo

    def delete(self, vehiculo: Vehiculo) -> None:
        self.db.delete(vehiculo)
        self.db.commit()

    def count(self) -> int:
        return self.db.query(Vehiculo).count()
