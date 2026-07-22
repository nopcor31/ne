"""
Controlador MVC para la evaluacion técnica por Area Medica con señales Qt.
"""

from typing import Optional
from PySide6.QtCore import QObject, Signal, Slot
from core.session_manager import session_manager
from services.area_medica_service import AreaMedicaService


class AreaMedicaController(QObject):
    """Controlador para orquestar envios, aprobaciones y revisiones técnicas médicas mediante señales Qt."""

    enviado_a_area = Signal(object)
    respuesta_registrada = Signal(object)
    pendientes_cargados = Signal(list)
    error_ocurrido = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

    @Slot(int, int, int)
    def enviar_a_area(self, cotizacion_id: int, area_medica_id: int, usuario_id: int):
        """Envia una cotizacion a revision del area medica correspondiente."""
        try:
            with session_manager.session_scope() as session:
                service = AreaMedicaService(session)
                envio = service.enviar_a_area_medica(cotizacion_id, area_medica_id, usuario_id)
                self.enviado_a_area.emit(envio)
                return envio
        except Exception as e:
            self.error_ocurrido.emit(str(e))
            raise

    @Slot(int, bool, int, str)
    def responder_revision(
        self,
        envio_id: int,
        aprobado: bool,
        usuario_id: int,
        observaciones: Optional[str] = None
    ):
        """Registra el dictamen de aprobacion o rechazo técnico del area medica."""
        try:
            with session_manager.session_scope() as session:
                service = AreaMedicaService(session)
                envio = service.registrar_respuesta_area_medica(envio_id, aprobado, usuario_id, observaciones)
                self.respuesta_registrada.emit(envio)
                return envio
        except Exception as e:
            self.error_ocurrido.emit(str(e))
            raise

    @Slot(object)
    def obtener_envios_pendientes(self, area_medica_id: Optional[int] = None):
        """Obtiene las revisiones medicas pendientes."""
        try:
            with session_manager.session_scope() as session:
                service = AreaMedicaService(session)
                pendientes = service.obtener_envios_pendientes(area_medica_id)
                self.pendientes_cargados.emit(pendientes)
                return pendientes
        except Exception as e:
            self.error_ocurrido.emit(str(e))
            raise

    @Slot(int)
    def obtener_historial_envios(self, cotizacion_id: int):
        """Obtiene el historial de revisiones medicas de una cotizacion."""
        try:
            with session_manager.session_scope() as session:
                service = AreaMedicaService(session)
                return service.obtener_historial_envios(cotizacion_id)
        except Exception as e:
            self.error_ocurrido.emit(str(e))
            raise
