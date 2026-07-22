"""
Controlador MVC para interacciones y tareas CRM con señales Qt.
"""

from typing import Optional
from PySide6.QtCore import QObject, Signal, Slot
from core.session_manager import session_manager
from services.crm_service import CRMService
from core.enums import TipoInteraccionCRM, PrioridadTarea


class CRMController(QObject):
    """Controlador para la gestion de interacciones CRM y tareas de seguimiento mediante señales Qt."""

    interaccion_registrada = Signal(object)
    tarea_creada = Signal(object)
    tarea_completada = Signal(int)
    interacciones_cargadas = Signal(list)
    tareas_cargadas = Signal(list)
    error_ocurrido = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

    @Slot(int, object, str, int, str)
    def registrar_interaccion(
        self,
        cliente_id: int,
        tipo: TipoInteraccionCRM,
        asunto: str,
        usuario_id: int,
        descripcion: Optional[str] = None
    ):
        """Registra una interaccion con cliente en la bitacora CRM."""
        try:
            with session_manager.session_scope() as session:
                service = CRMService(session)
                interaccion = service.registrar_interaccion(cliente_id, tipo, asunto, usuario_id, descripcion)
                self.interaccion_registrada.emit(interaccion)
                return interaccion
        except Exception as e:
            self.error_ocurrido.emit(str(e))
            raise

    @Slot(str, object, int, int, object, str, int)
    def crear_tarea(
        self,
        titulo: str,
        fecha_vencimiento,
        usuario_asignado_id: int,
        usuario_creador_id: int,
        prioridad: PrioridadTarea,
        descripcion: Optional[str] = None,
        cliente_id: Optional[int] = None
    ):
        """Crea una tarea de seguimiento asignada a un usuario."""
        try:
            with session_manager.session_scope() as session:
                service = CRMService(session)
                tarea = service.crear_tarea(
                    titulo, fecha_vencimiento, usuario_asignado_id,
                    usuario_creador_id, prioridad, descripcion, cliente_id
                )
                self.tarea_creada.emit(tarea)
                return tarea
        except Exception as e:
            self.error_ocurrido.emit(str(e))
            raise

    @Slot(int)
    def listar_interacciones_cliente(self, cliente_id: int):
        """Lista el historial de interacciones de un cliente."""
        try:
            with session_manager.session_scope() as session:
                service = CRMService(session)
                interacciones = service.listar_interacciones_cliente(cliente_id)
                self.interacciones_cargadas.emit(interacciones)
                return interacciones
        except Exception as e:
            self.error_ocurrido.emit(str(e))
            raise

    @Slot(int)
    def listar_tareas_usuario(self, usuario_id: int):
        """Lista las tareas pendientes asignadas a un usuario."""
        try:
            with session_manager.session_scope() as session:
                service = CRMService(session)
                tareas = service.listar_tareas_usuario(usuario_id)
                self.tareas_cargadas.emit(tareas)
                return tareas
        except Exception as e:
            self.error_ocurrido.emit(str(e))
            raise

    @Slot(int, int)
    def completar_tarea(self, tarea_id: int, usuario_id: int):
        """Marca una tarea de seguimiento como completada."""
        try:
            with session_manager.session_scope() as session:
                service = CRMService(session)
                tarea = service.completar_tarea(tarea_id, usuario_id)
                self.tarea_completada.emit(tarea_id)
                return tarea
        except Exception as e:
            self.error_ocurrido.emit(str(e))
            raise
