"""
Repositorio especializado para la entidad Factura.
"""

from datetime import date
from typing import Optional, List
from sqlalchemy import select, and_
from sqlalchemy.orm import Session
from models.factura import Factura
from core.enums import EstadoFactura
from repositories.base_repository import BaseRepository


class FacturaRepository(BaseRepository[Factura]):
    """Repositorio de acceso a datos para Facturas de cobro."""

    def __init__(self, db_session: Session):
        super().__init__(Factura, db_session)

    def obtener_por_cotizacion(self, cotizacion_id: int) -> Optional[Factura]:
        """Obtiene la factura emitida para una cotizacion."""
        stmt = select(Factura).where(Factura.cotizacion_id == cotizacion_id)
        return self.session.scalar(stmt)

    def obtener_vencidas(self, fecha_referencia: date) -> List[Factura]:
        """Obtiene las facturas emitidas no pagadas cuya fecha de vencimiento expiró."""
        stmt = (
            select(Factura)
            .where(
                and_(
                    Factura.estado == EstadoFactura.FACTURADA,
                    Factura.fecha_vencimiento < fecha_referencia
                )
            )
            .order_by(Factura.fecha_vencimiento.asc())
        )
        return list(self.session.scalars(stmt).all())
