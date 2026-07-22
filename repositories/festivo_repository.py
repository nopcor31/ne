"""
Repositorio especializado para la entidad Festivo.
"""

from datetime import date
from typing import List, Optional
from sqlalchemy import select, extract, and_
from sqlalchemy.orm import Session
from models.festivo import Festivo
from repositories.base_repository import BaseRepository


class FestivoRepository(BaseRepository[Festivo]):
    """Repositorio de acceso a datos para el calendario de dias festivos nacionales/locales."""

    def __init__(self, db_session: Session):
        super().__init__(Festivo, db_session)

    def es_festivo(self, fecha_evaluar: date) -> bool:
        """Determina si una fecha dada esta registrada como dia festivo."""
        stmt = select(Festivo).where(Festivo.fecha == fecha_evaluar)
        registro = self.session.scalar(stmt)
        return registro is not None

    def obtener_por_anio(self, anio: int) -> List[Festivo]:
        """Obtiene todos los dias festivos registrados para un año especifico."""
        stmt = (
            select(Festivo)
            .where(extract('year', Festivo.fecha) == anio)
            .order_by(Festivo.fecha.asc())
        )
        return list(self.session.scalars(stmt).all())

    def obtener_por_rango(self, fecha_inicio: date, fecha_fin: date) -> List[Festivo]:
        """Obtiene los festivos comprendidos en un rango de fechas especifico."""
        stmt = (
            select(Festivo)
            .where(
                and_(
                    Festivo.fecha >= fecha_inicio,
                    Festivo.fecha <= fecha_fin
                )
            )
            .order_by(Festivo.fecha.asc())
        )
        return list(self.session.scalars(stmt).all())
