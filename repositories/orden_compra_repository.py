"""
Repositorio especializado para la entidad OrdenCompra.
"""

from typing import Optional, List
from sqlalchemy import select
from sqlalchemy.orm import Session
from models.orden_compra import OrdenCompra
from core.enums import EstadoOrdenCompra
from repositories.base_repository import BaseRepository


class OrdenCompraRepository(BaseRepository[OrdenCompra]):
    """Repositorio de acceso a datos para Ordenes de Compra."""

    def __init__(self, db_session: Session):
        super().__init__(OrdenCompra, db_session)

    def obtener_por_cotizacion(self, cotizacion_id: int) -> Optional[OrdenCompra]:
        """Obtiene el registro de Orden de Compra asociado a una cotizacion."""
        stmt = select(OrdenCompra).where(OrdenCompra.cotizacion_id == cotizacion_id)
        return self.session.scalar(stmt)

    def obtener_solicitadas(self) -> List[OrdenCompra]:
        """Obtiene todas las Ordenes de Compra pendientes de recepcion."""
        stmt = (
            select(OrdenCompra)
            .where(OrdenCompra.estado == EstadoOrdenCompra.SOLICITADA)
            .order_by(OrdenCompra.fecha_solicitud.asc())
        )
        return list(self.session.scalars(stmt).all())
