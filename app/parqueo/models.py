from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class Parqueo(Base):
    __tablename__ = "parqueos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String, nullable=False)
    cupos_maximos = Column(Integer, nullable=False)

    movimientos = relationship("Movimiento", back_populates="parqueo")
