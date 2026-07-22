"""
Controlador MVC para la gestion de Alertas con señales Qt.
"""

from PySide6.QtCore import QObject, Signal, Slot
from core.session_manager import session_manager
from services.alerta_service import AlertaService


class AlertaController(QObject):
    """Controlador para evaluar, listar y descartar alertas automatizadas mediante señales Qt."""

    alertas_evaluadas = Signal(list)
    alertas_cargadas = Signal(list)
    alerta_descartada = Signal(int)
    alerta_resuelta = Signal(int)
    error_ocurrido = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

    @Slot(int)
    def evaluar_alertas(self, usuario_id: int):
        """Ejecuta el motor de reglas de alertas para el usuario especificado."""
        try:
            with session_manager.session_scope() as session:
                service = AlertaService(session)
                alertas = service.evaluar_y_generar_alertas(usuario_id)
                self.alertas_evaluadas.emit(alertas)
                return alertas
        except Exception as e:
            self.error_ocurrido.emit(str(e))
            raise

    @Slot(int)
    def obtener_alertas_activas(self, usuario_id: int):
        """Obtiene las alertas no leidas ni resueltas del usuario."""
        try:
            with session_manager.session_scope() as session:
                service = AlertaService(session)
                alertas = service.obtener_alertas_activas(usuario_id)
                self.alertas_cargadas.emit(alertas)
                return alertas
        except Exception as e:
            self.error_ocurrido.emit(str(e))
            raise

    @Slot(int)
    def descartar_alerta(self, alerta_id: int):
        """Descarta o marca como leida una alerta."""
        try:
            with session_manager.session_scope() as session:
                service = AlertaService(session)
                service.descartar_alerta(alerta_id)
                self.alerta_descartada.emit(alerta_id)
        except Exception as e:
            self.error_ocurrido.emit(str(e))
            raise

    @Slot(int)
    def resolver_alerta(self, alerta_id: int):
        """Marca una alerta como resuelta."""
        try:
            with session_manager.session_scope() as session:
                service = AlertaService(session)
                service.resolver_alerta(alerta_id)
                self.alerta_resuelta.emit(alerta_id)
        except Exception as e:
            self.error_ocurrido.emit(str(e))
            raise
