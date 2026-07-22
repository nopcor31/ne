"""
Controlador MVC para la bitácora de Historial de Actividad con señales Qt.
"""

from PySide6.QtCore import QObject, Signal, Slot
from core.session_manager import session_manager
from services.historial_service import HistorialService


class HistorialController(QObject):
    """Controlador para consulta de la bitácora de trazabilidad mediante señales Qt."""

    historial_cargado = Signal(list)
    error_ocurrido = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

    @Slot(int)
    def obtener_historial_reciente(self, limite: int = 50):
        """Obtiene las entradas mas recientes del historial de auditoria."""
        try:
            with session_manager.session_scope() as session:
                service = HistorialService(session)
                historial = service.obtener_recientes(limite)
                self.historial_cargado.emit(historial)
                return historial
        except Exception as e:
            self.error_ocurrido.emit(str(e))
            raise

    @Slot(str, int)
    def obtener_historial_entidad(self, entidad_tipo: str, entidad_id: int):
        """Obtiene el historial filtrado para un objeto de negocio especifico."""
        try:
            with session_manager.session_scope() as session:
                service = HistorialService(session)
                historial = service.obtener_por_entidad(entidad_tipo, entidad_id)
                self.historial_cargado.emit(historial)
                return historial
        except Exception as e:
            self.error_ocurrido.emit(str(e))
            raise
