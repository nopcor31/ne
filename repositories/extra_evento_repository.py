"""
Repositorio especializado para la entidad ExtraEvento.
"""

from typing import List
from sqlalchemy import select
from sqlalchemy.orm import Session
from models.extra_evento import ExtraEvento
from repositories.base_repository import BaseRepository


class ExtraEventoRepository(BaseRepository[ExtraEvento]):
    """Repositorio de acceso a datos para recargos y componentes extra de eventos."""

    def __init__(self, db_session: Session):
        super().__init__(ExtraEvento, db_session)

    def obtener_por_evento(self, evento_id: int) -> List[ExtraEvento]:
        """Obtiene todos los recargos extras asociados a un evento especifico."""
        stmt = (
            select(ExtraEvento)
            .where(ExtraEvento.evento_id == evento_id)
            .order_by(ExtraEvento.id.asc())
        )
        return list(self.session.scalars(stmt).all())
