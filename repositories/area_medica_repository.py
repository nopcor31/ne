"""
Repositorio especializado para la entidad AreaMedica.
"""

from typing import List
from sqlalchemy import select
from sqlalchemy.orm import Session
from models.area_medica import AreaMedica
from repositories.base_repository import BaseRepository


class AreaMedicaRepository(BaseRepository[AreaMedica]):
    """Repositorio de acceso a datos para areas medicas evaluadoras."""

    def __init__(self, db_session: Session):
        super().__init__(AreaMedica, db_session)

    def obtener_activas(self) -> List[AreaMedica]:
        """Obtiene la lista de areas medicas activas."""
        stmt = select(AreaMedica).where(AreaMedica.activo.is_(True)).order_by(AreaMedica.nombre)
        return list(self.session.scalars(stmt).all())
