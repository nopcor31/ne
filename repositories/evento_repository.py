"""
Repositorio especializado para la entidad Evento.
"""

from typing import List
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload
from models.evento import Evento
from repositories.base_repository import BaseRepository


class EventoRepository(BaseRepository[Evento]):
    """Repositorio de acceso a datos para eventos dentro de cotizaciones."""

    def __init__(self, db_session: Session):
        super().__init__(Evento, db_session)

    def obtener_por_cotizacion(self, cotizacion_id: int) -> List[Evento]:
        """Obtiene todos los eventos ordenados por su posicion en una cotizacion."""
        stmt = (
            select(Evento)
            .options(
                joinedload(Evento.servicio),
                joinedload(Evento.ciudad),
                joinedload(Evento.extras)
            )
            .where(Evento.cotizacion_id == cotizacion_id)
            .order_by(Evento.orden.asc())
        )
        return list(self.session.scalars(stmt).unique().all())
