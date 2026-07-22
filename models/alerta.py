"""
Modelo ORM para la entidad Alerta.
"""

from datetime import datetime
from typing import Optional, TYPE_CHECKING
from sqlalchemy import String, Text, Boolean, DateTime, ForeignKey, Enum as SQLEnum, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from core.database import Base
from core.enums import TipoAlerta, PrioridadAlerta

if TYPE_CHECKING:
    from models.usuario import Usuario


class Alerta(Base):
    """Representa un aviso o notificacion generada proactivamente por el sistema."""
    __tablename__ = "alerta"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    tipo: Mapped[TipoAlerta] = mapped_column(
        SQLEnum(TipoAlerta, name="tipo_alerta_enum"), nullable=False, index=True
    )
    titulo: Mapped[str] = mapped_column(String(300), nullable=False)
    mensaje: Mapped[str] = mapped_column(Text, nullable=False)
    entidad_tipo: Mapped[str] = mapped_column(String(50), nullable=False)  # "cotizacion", "tarea", etc.
    entidad_id: Mapped[int] = mapped_column(nullable=False)
    prioridad: Mapped[PrioridadAlerta] = mapped_column(
        SQLEnum(PrioridadAlerta, name="prioridad_alerta_enum"), default=PrioridadAlerta.ADVERTENCIA, nullable=False
    )
    fecha_creacion: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), nullable=False
    )
    fecha_visto: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuario.id", ondelete="CASCADE"), nullable=False)
    activa: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False, index=True)

    # Relaciones
    usuario: Mapped["Usuario"] = relationship("Usuario")

    def __repr__(self) -> str:
        return f"<Alerta(id={self.id}, tipo='{self.tipo}', titulo='{self.titulo}', activa={self.activa})>"
