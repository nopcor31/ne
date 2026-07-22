"""
Repositorio especializado para la entidad Tarea.
"""

from datetime import datetime
from typing import List
from sqlalchemy import select, and_
from sqlalchemy.orm import Session
from models.tarea import Tarea
from repositories.base_repository import BaseRepository


class TareaRepository(BaseRepository[Tarea]):
    """Repositorio de acceso a datos para tareas y recordatorios."""

    def __init__(self, db_session: Session):
        super().__init__(Tarea, db_session)

    def obtener_pendientes_por_usuario(self, usuario_id: int) -> List[Tarea]:
        """Obtiene las tareas pendientes asignadas a un usuario."""
        stmt = (
            select(Tarea)
            .where(
                Tarea.usuario_asignado_id == usuario_id,
                Tarea.completada.is_(False)
            )
            .order_by(Tarea.fecha_vencimiento.asc())
        )
        return list(self.session.scalars(stmt).all())

    def obtener_vencidas(self, fecha_referencia: datetime) -> List[Tarea]:
        """Obtiene las tareas sin completar cuya fecha de vencimiento es anterior a la referencia."""
        stmt = (
            select(Tarea)
            .where(
                and_(
                    Tarea.completada.is_(False),
                    Tarea.fecha_vencimiento < fecha_referencia
                )
            )
            .order_by(Tarea.fecha_vencimiento.asc())
        )
        return list(self.session.scalars(stmt).all())
