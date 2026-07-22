"""
Controlador MVC para el seguimiento de Ordenes de Compra con señales Qt.
"""

from typing import Optional
from PySide6.QtCore import QObject, Signal, Slot
from core.session_manager import session_manager
from services.orden_compra_service import OrdenCompraService


class OCController(QObject):
    """Controlador para solicitudes y recepciones de Ordenes de Compra mediante señales Qt."""

    oc_solicitada = Signal(object)
    oc_recibida = Signal(object)
    pendientes_oc_cargadas = Signal(list)
    error_ocurrido = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

    @Slot(int, int)
    def solicitar_oc(self, cotizacion_id: int, usuario_id: int):
        """Registra la solicitud formal de Orden de Compra al cliente."""
        try:
            with session_manager.session_scope() as session:
                service = OrdenCompraService(session)
                oc = service.solicitar_orden_compra(cotizacion_id, usuario_id)
                self.oc_solicitada.emit(oc)
                return oc
        except Exception as e:
            self.error_ocurrido.emit(str(e))
            raise

    @Slot(int, str, int, str, str)
    def registrar_recibido_oc(
        self,
        cotizacion_id: int,
        numero_oc: str,
        usuario_id: int,
        archivo_path: Optional[str] = None,
        observaciones: Optional[str] = None
    ):
        """Registra la recepcion formal de la Orden de Compra emitida por el cliente."""
        try:
            with session_manager.session_scope() as session:
                service = OrdenCompraService(session)
                oc = service.registrar_oc_recibida(cotizacion_id, numero_oc, usuario_id, archivo_path, observaciones)
                self.oc_recibida.emit(oc)
                return oc
        except Exception as e:
            self.error_ocurrido.emit(str(e))
            raise

    @Slot()
    def obtener_ordenes_compra_pendientes(self):
        """Obtiene las cotizaciones pendientes por recepcion de Orden de Compra."""
        try:
            with session_manager.session_scope() as session:
                service = OrdenCompraService(session)
                pendientes = service.obtener_ordenes_compra_pendientes()
                self.pendientes_oc_cargadas.emit(pendientes)
                return pendientes
        except Exception as e:
            self.error_ocurrido.emit(str(e))
            raise
