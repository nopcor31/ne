"""
Servicio para la administracion de Facturacion y Cobros.
"""

from typing import Optional
from datetime import date
from sqlalchemy.orm import Session
from models.factura import Factura
from repositories.factura_repository import FacturaRepository
from repositories.cotizacion_repository import CotizacionRepository
from services.estado_service import EstadoService
from core.enums import EstadoFactura, EstadoCotizacion


class FacturacionService:
    """Servicio para emision de facturas y registro de pagos recibidos."""

    def __init__(self, session: Session):
        self.session = session
        self.factura_repo = FacturaRepository(session)
        self.cotizacion_repo = CotizacionRepository(session)
        self.estado_service = EstadoService(session)

    def emitir_factura(
        self,
        cotizacion_id: int,
        numero_factura: str,
        fecha_facturacion: date,
        fecha_vencimiento: date,
        usuario_id: int,
        observaciones: Optional[str] = None
    ) -> Factura:
        """Registra la emision formal de la factura de cobro."""
        cotizacion = self.cotizacion_repo.get_by_id_or_fail(cotizacion_id)

        factura = Factura(
            cotizacion_id=cotizacion_id,
            numero_factura=numero_factura,
            fecha_facturacion=fecha_facturacion,
            fecha_vencimiento=fecha_vencimiento,
            valor_facturado=cotizacion.valor_total,
            observaciones=observaciones,
            estado=EstadoFactura.FACTURADA
        )
        self.factura_repo.create(factura)
        self.session.flush()

        # Avanzar cotizacion a PENDIENTE_FACTURACION si venia de OC_RECIBIDA, luego FACTURADA
        if cotizacion.estado == EstadoCotizacion.OC_RECIBIDA:
            self.estado_service.transicionar(
                cotizacion_id, EstadoCotizacion.PENDIENTE_FACTURACION, usuario_id
            )

        self.estado_service.transicionar(cotizacion_id, EstadoCotizacion.FACTURADA, usuario_id)
        return factura

    def registrar_pago_recibido(
        self, cotizacion_id: int, fecha_pago: date, usuario_id: int
    ) -> Factura:
        """Registra el pago efectivo de la factura enviada."""
        factura = self.factura_repo.obtener_por_cotizacion(cotizacion_id)
        if not factura:
            raise ValueError(f"No se encontro factura registrada para la cotizacion #{cotizacion_id}")

        factura.fecha_pago = fecha_pago
        factura.estado = EstadoFactura.PAGADA
        self.session.flush()

        self.estado_service.transicionar(cotizacion_id, EstadoCotizacion.PAGADA, usuario_id)
        return factura
