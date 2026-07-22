"""
Controlador MVC para la agenda operativa y programacion de servicios con señales Qt.
"""

from datetime import date
from typing import Optional
from PySide6.QtCore import QObject, Signal, Slot
from core.session_manager import session_manager
from services.programacion_service import ProgramacionService


class ProgramacionController(QObject):
    """Controlador para agendar servicios, sincronizar con Outlook y consultar la agenda mediante señales Qt."""

    servicio_programado = Signal(object)
    agenda_cargada = Signal(list)
    programacion_cancelada = Signal(int)
    outlook_sincronizado = Signal(bool)
    error_ocurrido = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

    @Slot(int, int, object, str, int, str)
    def programar_servicio(
        self,
        cotizacion_id: int,
        evento_id: int,
        fecha_programada: date,
        recurso_asignado: str,
        usuario_id: int,
        notas: Optional[str] = None
    ):
        """Programa la ejecucion de un evento medico en la agenda operativa."""
        try:
            with session_manager.session_scope() as session:
                service = ProgramacionService(session)
                programacion = service.programar_evento(
                    cotizacion_id, evento_id, fecha_programada, recurso_asignado, usuario_id, notas
                )
                self.servicio_programado.emit(programacion)
                return programacion
        except Exception as e:
            self.error_ocurrido.emit(str(e))
            raise

    @Slot(object, object)
    def obtener_agenda(self, fecha_inicio: date, fecha_fin: date):
        """Obtiene la lista de servicios programados en un rango de fechas."""
        try:
            with session_manager.session_scope() as session:
                service = ProgramacionService(session)
                agenda = service.obtener_programacion_rango(fecha_inicio, fecha_fin)
                self.agenda_cargada.emit(agenda)
                return agenda
        except Exception as e:
            self.error_ocurrido.emit(str(e))
            raise

    @Slot(int, int)
    def cancelar_programacion(self, programacion_id: int, usuario_id: int):
        """Cancela un agendamiento de servicio."""
        try:
            with session_manager.session_scope() as session:
                service = ProgramacionService(session)
                service.cancelar_programacion(programacion_id, usuario_id)
                self.programacion_cancelada.emit(programacion_id)
        except Exception as e:
            self.error_ocurrido.emit(str(e))
            raise

    @Slot(int)
    def sincronizar_outlook(self, programacion_id: int) -> bool:
        """Sincroniza una programacion con el calendario de Outlook via COM."""
        try:
            with session_manager.session_scope() as session:
                service = ProgramacionService(session)
                exito = service.sincronizar_outlook(programacion_id)
                self.outlook_sincronizado.emit(exito)
                return exito
        except Exception as e:
            self.error_ocurrido.emit(str(e))
            raise
