"""
Repositorio especializado para la entidad EnvioAreaMedica.
"""

from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.orm import Session
from models.envio_area_medica import EnvioAreaMedica
from repositories.base_repository import BaseRepository


class EnvioAreaMedicaRepository(BaseRepository[EnvioAreaMedica]):
    """Repositorio de acceso a datos para envios de aprobacion a area medica."""

    def __init__(self, db_session: Session):
        super().__init__(EnvioAreaMedica, db_session)

    def obtener_ultimo_envio(self, cotizacion_id: int) -> Optional[EnvioAreaMedica]:
        """Obtiene el registro de envio a area medica mas reciente para una cotizacion."""
        stmt = (
            select(EnvioAreaMedica)
            .where(EnvioAreaMedica.cotizacion_id == cotizacion_id)
            .order_by(EnvioAreaMedica.fecha_envio.desc())
        )
        return self.session.scalar(stmt)

    def obtener_pendientes(self) -> List[EnvioAreaMedica]:
        """Obtiene los envios a area medica que aun no han sido aprobados ni rechazados."""
        stmt = (
            select(EnvioAreaMedica)
            .where(EnvioAreaMedica.aprobado.is_(None))
            .order_by(EnvioAreaMedica.fecha_envio.asc())
        )
        return list(self.session.scalars(stmt).all())
