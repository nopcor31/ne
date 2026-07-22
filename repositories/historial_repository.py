"""
Repositorio especializado para la entidad HistorialActividad.
"""

from typing import List, Optional
from sqlalchemy import select, and_
from sqlalchemy.orm import Session, joinedload
from models.historial_actividad import HistorialActividad
from repositories.base_repository import BaseRepository


class HistorialRepository(BaseRepository[HistorialActividad]):
    """Repositorio de acceso a datos para la bitácora de actividad."""

    def __init__(self, db_session: Session):
        super().__init__(HistorialActividad, db_session)

    def obtener_recientes(self, limite: int = 50) -> List[HistorialActividad]:
        """Obtiene las actividades mas recientes registradas en la bitacora."""
        stmt = (
            select(HistorialActividad)
            .options(joinedload(HistorialActividad.usuario))
            .order_by(HistorialActividad.fecha_hora.desc())
            .limit(limite)
        )
        return list(self.session.scalars(stmt).all())

    def obtener_por_entidad(self, entidad_tipo: str, entidad_id: int) -> List[HistorialActividad]:
        """Obtiene la trazabilidad completa de una entidad especifica."""
        stmt = (
            select(HistorialActividad)
            .options(joinedload(HistorialActividad.usuario))
            .where(
                and_(
                    HistorialActividad.entidad_tipo == entidad_tipo,
                    HistorialActividad.entidad_id == entidad_id
                )
            )
            .order_by(HistorialActividad.fecha_hora.desc())
        )
        return list(self.session.scalars(stmt).all())
