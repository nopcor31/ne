"""
Repositorio especializado para la entidad InteraccionCRM.
"""

from typing import List
from sqlalchemy import select
from sqlalchemy.orm import Session
from models.interaccion_crm import InteraccionCRM
from repositories.base_repository import BaseRepository


class InteraccionRepository(BaseRepository[InteraccionCRM]):
    """Repositorio de acceso a datos para interacciones del CRM."""

    def __init__(self, db_session: Session):
        super().__init__(InteraccionCRM, db_session)

    def obtener_por_cliente(self, cliente_id: int) -> List[InteraccionCRM]:
        """Obtiene las interacciones de un cliente ordenadas cronológicamente."""
        stmt = (
            select(InteraccionCRM)
            .where(InteraccionCRM.cliente_id == cliente_id)
            .order_by(InteraccionCRM.fecha_hora.desc())
        )
        return list(self.session.scalars(stmt).all())

    def obtener_por_cotizacion(self, cotizacion_id: int) -> List[InteraccionCRM]:
        """Obtiene las interacciones asociadas a una cotización específica."""
        stmt = (
            select(InteraccionCRM)
            .where(InteraccionCRM.cotizacion_id == cotizacion_id)
            .order_by(InteraccionCRM.fecha_hora.desc())
        )
        return list(self.session.scalars(stmt).all())
