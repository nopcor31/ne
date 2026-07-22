"""
Controlador MVC para el Dashboard principal con señales Qt.
"""

from PySide6.QtCore import QObject, Signal, Slot
from core.session_manager import session_manager
from services.dashboard_service import DashboardService
from services.historial_service import HistorialService
from services.dto.dashboard_dto import DashboardMetricsDTO


class DashboardController(QObject):
    """Controlador encargado de proveer datos consolidados al Dashboard mediante señales Qt."""

    metricas_cargadas = Signal(object)
    actividad_cargada = Signal(object)
    error_ocurrido = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

    @Slot()
    def obtener_metricas_dashboard(self) -> DashboardMetricsDTO:
        """Obtiene el DTO con todas las metricas y KPIs del sistema."""
        try:
            with session_manager.session_scope() as session:
                service = DashboardService(session)
                metricas = service.obtener_metricas()
                self.metricas_cargadas.emit(metricas)
                return metricas
        except Exception as e:
            self.error_ocurrido.emit(str(e))
            raise

    @Slot(int)
    def obtener_actividad_reciente(self, limite: int = 20):
        """Obtiene la lista de eventos recientes para el feed de actividad."""
        try:
            with session_manager.session_scope() as session:
                service = HistorialService(session)
                actividad = service.obtener_recientes(limite)
                self.actividad_cargada.emit(actividad)
                return actividad
        except Exception as e:
            self.error_ocurrido.emit(str(e))
            raise

    @Slot()
    def obtener_resumen_mensual(self):
        """Obtiene resumen operativo mensual."""
        try:
            with session_manager.session_scope() as session:
                service = DashboardService(session)
                resumen = service.obtener_resumen_mensual()
                return resumen
        except Exception as e:
            self.error_ocurrido.emit(str(e))
            raise
