"""
Modelo ORM para la entidad OrdenCompra.
"""

from datetime import datetime
from typing import Optional, TYPE_CHECKING
from sqlalchemy import String, Text, DateTime, ForeignKey, Enum as SQLEnum, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from core.database import Base
from core.enums import EstadoOrdenCompra

if TYPE_CHECKING:
    from models.cotizacion import Cotizacion


class OrdenCompra(Base):
    """Representa el seguimiento de la Orden de Compra (OC) entregada por el cliente."""
    __tablename__ = "orden_compra"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    cotizacion_id: Mapped[int] = mapped_column(
        ForeignKey("cotizacion.id", ondelete="CASCADE"), nullable=False
    )
    numero_oc: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, index=True)
    fecha_solicitud: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), nullable=False
    )
    fecha_recibido: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    archivo_path: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    observaciones: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    estado: Mapped[EstadoOrdenCompra] = mapped_column(
        SQLEnum(EstadoOrdenCompra, name="estado_oc_enum"),
        default=EstadoOrdenCompra.SOLICITADA,
        nullable=False
    )

    # Relaciones
    cotizacion: Mapped["Cotizacion"] = relationship("Cotizacion", back_populates="ordenes_compra")

    def __repr__(self) -> str:
        return f"<OrdenCompra(id={self.id}, numero='{self.numero_oc}', estado='{self.estado}')>"
