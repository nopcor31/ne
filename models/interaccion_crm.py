"""
Modelo ORM para la entidad InteraccionCRM.
"""

from datetime import datetime
from typing import Optional, TYPE_CHECKING
from sqlalchemy import String, Text, DateTime, ForeignKey, Enum as SQLEnum, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from core.database import Base
from core.enums import TipoInteraccionCRM

if TYPE_CHECKING:
    from models.cliente import Cliente
    from models.cotizacion import Cotizacion
    from models.usuario import Usuario


class InteraccionCRM(Base):
    """Representa una llamada, correo, reunion o visita registrada con un cliente."""
    __tablename__ = "interaccion_crm"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    cliente_id: Mapped[int] = mapped_column(ForeignKey("cliente.id", ondelete="CASCADE"), nullable=False)
    cotizacion_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("cotizacion.id", ondelete="SET NULL"), nullable=True
    )
    tipo: Mapped[TipoInteraccionCRM] = mapped_column(
        SQLEnum(TipoInteraccionCRM, name="tipo_interaccion_enum"), nullable=False
    )
    fecha_hora: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), nullable=False
    )
    asunto: Mapped[str] = mapped_column(String(300), nullable=False)
    descripcion: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuario.id", ondelete="RESTRICT"), nullable=False)

    # Relaciones
    cliente: Mapped["Cliente"] = relationship("Cliente", back_populates="interacciones")
    cotizacion: Mapped[Optional["Cotizacion"]] = relationship("Cotizacion", back_populates="interacciones")
    usuario: Mapped["Usuario"] = relationship("Usuario")

    def __repr__(self) -> str:
        return f"<InteraccionCRM(id={self.id}, tipo='{self.tipo}', asunto='{self.asunto}')>"
