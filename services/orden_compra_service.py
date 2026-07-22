"""
Servicio para el seguimiento y recepcion de Ordenes de Compra.
"""

from typing import Optional
from datetime import datetime
from sqlalchemy.orm import Session
from models.orden_compra import OrdenCompra
from repositories.orden_compra_repository import OrdenCompraRepository
from services.estado_service import EstadoService
from core.enums import EstadoOrdenCompra, EstadoCotizacion


class OrdenCompraService:
    """Servicio para el control de Ordenes de Compra enviadas por el cliente."""

    def __init__(self, session: Session):
        self.session = session
        self.oc_repo = OrdenCompraRepository(session)
        self.estado_service = EstadoService(session)

    def solicitar_orden_compra(self, cotizacion_id: int, usuario_id: int) -> OrdenCompra:
        """Registra la solicitud formal de Orden de Compra al cliente."""
        oc = OrdenCompra(
            cotizacion_id=cotizacion_id,
            fecha_solicitud=datetime.now(),
            estado=EstadoOrdenCompra.SOLICITADA
        )
        self.oc_repo.create(oc)
        self.session.flush()

        self.estado_service.transicionar(cotizacion_id, EstadoCotizacion.OC_SOLICITADA, usuario_id)
        return oc

    def registrar_oc_recibida(
        self,
        cotizacion_id: int,
        numero_oc: str,
        usuario_id: int,
        archivo_path: Optional[str] = None,
        observaciones: Optional[str] = None
    ) -> OrdenCompra:
        """Registra la recepcion efectiva de la Orden de Compra entregada por el cliente."""
        oc = self.oc_repo.obtener_por_cotizacion(cotizacion_id)
        if not oc:
            oc = OrdenCompra(cotizacion_id=cotizacion_id, fecha_solicitud=datetime.now())
            self.oc_repo.create(oc)

        oc.numero_oc = numero_oc
        oc.fecha_recibido = datetime.now()
        oc.archivo_path = archivo_path
        oc.observaciones = observaciones
        oc.estado = EstadoOrdenCompra.RECIBIDA
        self.session.flush()

        self.estado_service.transicionar(cotizacion_id, EstadoCotizacion.OC_RECIBIDA, usuario_id)
        return oc
