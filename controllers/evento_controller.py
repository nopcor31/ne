"""
Controlador MVC para gestion de Eventos en Cotizaciones con señales Qt.
"""

from typing import List, Dict, Any, Optional
from PySide6.QtCore import QObject, Signal, Slot
from core.session_manager import session_manager
from services.evento_service import EventoService


class EventoController(QObject):
    """Controlador para agregar, editar, calcular y eliminar eventos mediante señales Qt."""

    evento_guardado = Signal(int)
    evento_eliminado = Signal(int)
    eventos_cargados = Signal(list)
    error_ocurrido = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

    @Slot(int, int, int, object, object, object, str, str, str, str, object, object)
    def guardar_evento(
        self,
        cotizacion_id: int,
        servicio_id: int,
        ciudad_id: int,
        fecha,
        hora_inicio,
        hora_fin,
        direccion: str,
        contacto: str,
        telefono: str,
        observaciones: str = "",
        extras_data: Optional[List[Dict[str, Any]]] = None,
        evento_id: Optional[int] = None
    ) -> int:
        """Calcula tarifa y persiste un evento asociandolo a la cotizacion."""
        try:
            with session_manager.session_scope() as session:
                service = EventoService(session)
                evento = service.calcular_y_guardar_evento(
                    cotizacion_id=cotizacion_id,
                    servicio_id=servicio_id,
                    ciudad_id=ciudad_id,
                    fecha=fecha,
                    hora_inicio=hora_inicio,
                    hora_fin=hora_fin,
                    direccion=direccion,
                    contacto=contacto,
                    telefono=telefono,
                    observaciones=observaciones,
                    extras_data=extras_data,
                    evento_id=evento_id
                )
                self.evento_guardado.emit(evento.id)
                return evento.id
        except Exception as e:
            self.error_ocurrido.emit(str(e))
            raise

    @Slot(int)
    def eliminar_evento(self, evento_id: int):
        """Elimina un evento de la cotizacion."""
        try:
            with session_manager.session_scope() as session:
                service = EventoService(session)
                service.eliminar_evento(evento_id)
                self.evento_eliminado.emit(evento_id)
        except Exception as e:
            self.error_ocurrido.emit(str(e))
            raise

    @Slot(int)
    def obtener_eventos_cotizacion(self, cotizacion_id: int):
        """Obtiene todos los eventos pertenecientes a una cotizacion."""
        try:
            with session_manager.session_scope() as session:
                service = EventoService(session)
                eventos = service.obtener_eventos_cotizacion(cotizacion_id)
                self.eventos_cargados.emit(eventos)
                return eventos
        except Exception as e:
            self.error_ocurrido.emit(str(e))
            raise
