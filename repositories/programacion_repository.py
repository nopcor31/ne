"""
Repositorio especializado para la entidad Programacion.
"""

from datetime import date
from typing import List
from sqlalchemy import select, and_
from sqlalchemy.orm import Session
from models.programacion import Programacion
from repositories.base_repository import BaseRepository


class ProgramacionRepository(BaseRepository[Programacion]):
    """Repositorio de acceso a datos para la agenda de programaciones operativas."""

    def __init__(self, db_session: Session):
        super().__init__(Programacion, db_session)

    def obtener_por_rango_fechas(self, fecha_inicio: date, fecha_fin: date) -> List[Programacion]:
        """Obtiene las programaciones comprendidas dentro de un rango de fechas."""
        stmt = (
            select(Programacion)
            .where(
                and_(
                    Programacion.fecha_programada >= fecha_inicio,
                    Programacion.fecha_programada <= fecha_fin
                )
            )
            .order_by(Programacion.fecha_programada.asc(), Programacion.hora_inicio.asc())
        )
        return list(self.session.scalars(stmt).all())

    def obtener_por_cotizacion(self, cotizacion_id: int) -> List[Programacion]:
        """Obtiene todas las programaciones asociadas a un expediente de cotizacion."""
        stmt = (
            select(Programacion)
            .where(Programacion.cotizacion_id == cotizacion_id)
            .order_by(Programacion.fecha_programada.asc())
        )
        return list(self.session.scalars(stmt).all())
