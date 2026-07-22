"""
Repositorio especializado para la entidad Alerta.
"""

from typing import List, Optional
from sqlalchemy import select, and_
from sqlalchemy.orm import Session
from models.alerta import Alerta
from core.enums import TipoAlerta
from repositories.base_repository import BaseRepository


class AlertaRepository(BaseRepository[Alerta]):
    """Repositorio de acceso a datos para alertas del sistema."""

    def __init__(self, db_session: Session):
        super().__init__(Alerta, db_session)

    def obtener_activas_por_usuario(self, usuario_id: int) -> List[Alerta]:
        """Obtiene las alertas activas no descartadas para un usuario."""
        stmt = (
            select(Alerta)
            .where(
                and_(
                    Alerta.usuario_id == usuario_id,
                    Alerta.activa.is_(True)
                )
            )
            .order_by(Alerta.fecha_creacion.desc())
        )
        return list(self.session.scalars(stmt).all())

    def buscar_existente(
        self, tipo: TipoAlerta, entidad_tipo: str, entidad_id: int, usuario_id: int
    ) -> Optional[Alerta]:
        """Verifica si ya existe una alerta activa identica para evitar duplicacion."""
        stmt = select(Alerta).where(
            and_(
                Alerta.tipo == tipo,
                Alerta.entidad_tipo == entidad_tipo,
                Alerta.entidad_id == entidad_id,
                Alerta.usuario_id == usuario_id,
                Alerta.activa.is_(True)
            )
        )
        return self.session.scalar(stmt)
