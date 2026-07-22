"""
Controlador MVC para facturacion y cobros con señales Qt.
"""

from datetime import date
from typing import Optional
from PySide6.QtCore import QObject, Signal, Slot
from core.session_manager import session_manager
from services.facturacion_service import FacturacionService


class FacturacionController(QObject):
    """Controlador para emision de facturas y cobranza mediante señales Qt."""

    factura_emitida = Signal(object)
    pago_registrado = Signal(object)
    facturas_pendientes_cargadas = Signal(list)
    error_ocurrido = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

    @Slot(int, str, object, object, int, str)
    def emitir_factura(
        self,
        cotizacion_id: int,
        numero_factura: str,
        fecha_facturacion: date,
        fecha_vencimiento: date,
        usuario_id: int,
        observaciones: Optional[str] = None
    ):
        """Emite la factura asociada a una cotizacion aprobada."""
        try:
            with session_manager.session_scope() as session:
                service = FacturacionService(session)
                factura = service.emitir_factura(
                    cotizacion_id, numero_factura, fecha_facturacion, fecha_vencimiento, usuario_id, observaciones
                )
                self.factura_emitida.emit(factura)
                return factura
        except Exception as e:
            self.error_ocurrido.emit(str(e))
            raise

    @Slot(int, object, int)
    def registrar_pago(self, cotizacion_id: int, fecha_pago: date, usuario_id: int):
        """Registra el recaudo o pago recibido por concepto de una factura."""
        try:
            with session_manager.session_scope() as session:
                service = FacturacionService(session)
                factura = service.registrar_pago_recibido(cotizacion_id, fecha_pago, usuario_id)
                self.pago_registrado.emit(factura)
                return factura
        except Exception as e:
            self.error_ocurrido.emit(str(e))
            raise

    @Slot()
    def obtener_facturas_pendientes(self):
        """Obtiene las facturas pendientes de cobro/recaudo."""
        try:
            with session_manager.session_scope() as session:
                service = FacturacionService(session)
                pendientes = service.obtener_facturas_pendientes()
                self.facturas_pendientes_cargadas.emit(pendientes)
                return pendientes
        except Exception as e:
            self.error_ocurrido.emit(str(e))
            raise
