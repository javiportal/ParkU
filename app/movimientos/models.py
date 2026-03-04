import enum
from datetime import datetime

from sqlalchemy import Column, Integer, DateTime, Enum, ForeignKey, Index
from sqlalchemy.orm import relationship

from app.database import Base


class TipoMovimiento(str, enum.Enum):
    entrada = "entrada"
    salida = "salida"


class Movimiento(Base):
    __tablename__ = "movimientos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    fecha_hora = Column(DateTime, default=datetime.utcnow, nullable=False)
    tipo = Column(Enum(TipoMovimiento), nullable=False)
    vehiculo_id = Column(Integer, ForeignKey("vehiculos.id"), nullable=False)
    parqueo_id = Column(Integer, ForeignKey("parqueos.id"), nullable=False)

    vehiculo = relationship("Vehiculo", back_populates="movimientos")
    parqueo = relationship("Parqueo", back_populates="movimientos")

    __table_args__ = (
        Index("ix_movimientos_vehiculo_id", "vehiculo_id"),
        Index("ix_movimientos_fecha_hora", "fecha_hora"),
        Index("ix_movimientos_tipo", "tipo"),
    )
