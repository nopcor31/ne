"""
Modelo ORM para la entidad Factura.
"""

from datetime import date
from typing import Optional, TYPE_CHECKING
from sqlalchemy import String, Text, Numeric, Date, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from core.database import Base
from core.enums import EstadoFactura

if TYPE_CHECKING:
    from models.cotizacion import Cotizacion


class Factura(Base):
    """Representa la factura de cobro emitida al cliente tras la ejecucion del servicio."""
    __tablename__ = "factura"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    cotizacion_id: Mapped[int] = mapped_column(
        ForeignKey("cotizacion.id", ondelete="CASCADE"), nullable=False
    )
    numero_factura: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    fecha_facturacion: Mapped[date] = mapped_column(Date, nullable=False)
    fecha_vencimiento: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    fecha_pago: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    valor_facturado: Mapped[float] = mapped_column(Numeric(14, 2), nullable=False)
    observaciones: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    estado: Mapped[EstadoFactura] = mapped_column(
        SQLEnum(EstadoFactura, name="estado_factura_enum"),
        default=EstadoFactura.FACTURADA,
        nullable=False,
        index=True
    )

    # Relaciones
    cotizacion: Mapped["Cotizacion"] = relationship("Cotizacion", back_populates="facturas")

    def __repr__(self) -> str:
        return f"<Factura(id={self.id}, numero='{self.numero_factura}', estado='{self.estado}')>"
