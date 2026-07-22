"""
Servicio para el registro centralizado de la bitacora de actividad.
"""

from typing import Optional, List
from sqlalchemy.orm import Session
from models.historial_actividad import HistorialActividad
from repositories.historial_repository import HistorialRepository
from loguru import logger


class HistorialService:
    """Servicio encargado del registro transversal de trazabilidad."""

    def __init__(self, session: Session):
        self.session = session
        self.repo = HistorialRepository(session)

    def registrar_accion(
        self,
        usuario_id: int,
        entidad_tipo: str,
        entidad_id: int,
        accion: str,
        detalle: Optional[str] = None,
        es_automatico: bool = False
    ) -> HistorialActividad:
        """Registra un evento en la bitácora de actividad."""
        registro = HistorialActividad(
            usuario_id=usuario_id,
            entidad_tipo=entidad_tipo,
            entidad_id=entidad_id,
            accion=accion,
            detalle=detalle,
            es_automatico=es_automatico
        )
        creado = self.repo.create(registro)
        logger.info(f"Historial registrado [{entidad_tipo}:{entidad_id}] - {accion}")
        return creado

    def obtener_recientes(self, limite: int = 50) -> List[HistorialActividad]:
        """Obtiene las entradas mas recientes del historial."""
        return self.repo.obtener_recientes(limite)

    def obtener_por_entidad(self, entidad_tipo: str, entidad_id: int) -> List[HistorialActividad]:
        """Obtiene la trazabilidad completa de una entidad."""
        return self.repo.obtener_por_entidad(entidad_tipo, entidad_id)
