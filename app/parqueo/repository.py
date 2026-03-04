from sqlalchemy.orm import Session

from app.parqueo.models import Parqueo


class ParqueoRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, parqueo_id: int) -> Parqueo | None:
        return self.db.query(Parqueo).filter(Parqueo.id == parqueo_id).first()

    def get_all(self, skip: int = 0, limit: int = 20) -> list[Parqueo]:
        return self.db.query(Parqueo).offset(skip).limit(limit).all()

    def create(self, parqueo: Parqueo) -> Parqueo:
        self.db.add(parqueo)
        self.db.commit()
        self.db.refresh(parqueo)
        return parqueo

    def update(self, parqueo: Parqueo) -> Parqueo:
        self.db.commit()
        self.db.refresh(parqueo)
        return parqueo

    def count(self) -> int:
        return self.db.query(Parqueo).count()
