"""
Repositorio especializado para la entidad Cotizacion.
"""

from typing import List, Optional
from sqlalchemy import select, or_
from sqlalchemy.orm import Session, joinedload
from models.cotizacion import Cotizacion
from core.enums import EstadoCotizacion
from repositories.base_repository import BaseRepository


class CotizacionRepository(BaseRepository[Cotizacion]):
    """Repositorio de acceso a datos para expedientes de cotizacion."""

    def __init__(self, db_session: Session):
        super().__init__(Cotizacion, db_session)

    def obtener_con_detalles(self, cotizacion_id: int) -> Optional[Cotizacion]:
        """Obtiene una cotizacion con sus relaciones cargadas de forma ansiosa."""
        stmt = (
            select(Cotizacion)
            .options(
                joinedload(Cotizacion.cliente),
                joinedload(Cotizacion.contacto),
                joinedload(Cotizacion.usuario_creador),
                joinedload(Cotizacion.eventos)
            )
            .where(Cotizacion.id == cotizacion_id)
        )
        return self.session.scalar(stmt)

    def buscar_por_numero(self, numero_cotizacion: str) -> Optional[Cotizacion]:
        """Busca una cotizacion por su numero identificador (ej. COT-2026-0001)."""
        stmt = select(Cotizacion).where(Cotizacion.numero_cotizacion == numero_cotizacion)
        return self.session.scalar(stmt)

    def obtener_por_estado(self, estado: EstadoCotizacion) -> List[Cotizacion]:
        """Obtiene todas las cotizaciones en un estado especifico del pipeline."""
        stmt = (
            select(Cotizacion)
            .where(Cotizacion.estado == estado)
            .order_by(Cotizacion.fecha_creacion.desc())
        )
        return list(self.session.scalars(stmt).all())

    def obtener_por_cliente(self, cliente_id: int) -> List[Cotizacion]:
        """Obtiene todas las cotizaciones asociadas a un cliente."""
        stmt = (
            select(Cotizacion)
            .where(Cotizacion.cliente_id == cliente_id)
            .order_by(Cotizacion.fecha_creacion.desc())
        )
        return list(self.session.scalars(stmt).all())

    def buscar_por_texto(self, texto: str) -> List[Cotizacion]:
        """Busca cotizaciones por numero o por nombre de empresa del cliente."""
        patron = f"%{texto}%"
        stmt = (
            select(Cotizacion)
            .join(Cotizacion.cliente)
            .where(
                or_(
                    Cotizacion.numero_cotizacion.ilike(patron),
                    Cotizacion.cliente.has(empresa=patron)
                )
            )
            .order_by(Cotizacion.fecha_creacion.desc())
        )
        return list(self.session.scalars(stmt).all())
