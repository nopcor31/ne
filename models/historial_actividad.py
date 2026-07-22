"""
Modelo ORM para la entidad HistorialActividad.
"""

from datetime import datetime
from typing import Optional, TYPE_CHECKING
from sqlalchemy import String, Text, Boolean, DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from core.database import Base

if TYPE_CHECKING:
    from models.usuario import Usuario


class HistorialActividad(Base):
    """Bitacora imutable de auditoria y trazabilidad transversal de eventos en el CRM."""
    __tablename__ = "historial_actividad"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    fecha_hora: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), nullable=False, index=True
    )
    usuario_id: Mapped[int] = mapped_column(
        ForeignKey("usuario.id", ondelete="RESTRICT"), nullable=False, index=True
    )
    entidad_tipo: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    entidad_id: Mapped[int] = mapped_column(nullable=False, index=True)
    accion: Mapped[str] = mapped_column(String(300), nullable=False)
    detalle: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    es_automatico: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    # Relaciones
    usuario: Mapped["Usuario"] = relationship("Usuario", back_populates="actividades_historial")

    def __repr__(self) -> str:
        return (
            f"<HistorialActividad(id={self.id}, fecha='{self.fecha_hora}', "
            f"entidad='{self.entidad_tipo}:{self.entidad_id}', accion='{self.accion}')>"
        )
