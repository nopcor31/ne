"""
Modelo ORM para la entidad Tarea.
"""

from datetime import datetime
from typing import Optional, TYPE_CHECKING
from sqlalchemy import String, Text, Boolean, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from core.database import Base
from core.enums import PrioridadTarea

if TYPE_CHECKING:
    from models.cliente import Cliente
    from models.cotizacion import Cotizacion
    from models.usuario import Usuario


class Tarea(Base):
    """Representa una tarea o recordatorio vinculado a un cliente o cotizacion."""
    __tablename__ = "tarea"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    cliente_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("cliente.id", ondelete="CASCADE"), nullable=True
    )
    cotizacion_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("cotizacion.id", ondelete="CASCADE"), nullable=True
    )
    titulo: Mapped[str] = mapped_column(String(300), nullable=False)
    descripcion: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    prioridad: Mapped[PrioridadTarea] = mapped_column(
        SQLEnum(PrioridadTarea, name="prioridad_tarea_enum"), default=PrioridadTarea.MEDIA, nullable=False
    )
    fecha_vencimiento: Mapped[datetime] = mapped_column(DateTime, nullable=False, index=True)
    completada: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False, index=True)
    fecha_completada: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    usuario_asignado_id: Mapped[int] = mapped_column(
        ForeignKey("usuario.id", ondelete="RESTRICT"), nullable=False
    )
    usuario_creador_id: Mapped[int] = mapped_column(
        ForeignKey("usuario.id", ondelete="RESTRICT"), nullable=False
    )

    # Relaciones
    cliente: Mapped[Optional["Cliente"]] = relationship("Cliente", back_populates="tareas")
    cotizacion: Mapped[Optional["Cotizacion"]] = relationship("Cotizacion", back_populates="tareas")
    usuario_asignado: Mapped["Usuario"] = relationship(
        "Usuario", back_populates="tareas_asignadas", foreign_keys=[usuario_asignado_id]
    )
    usuario_creador: Mapped["Usuario"] = relationship("Usuario", foreign_keys=[usuario_creador_id])

    def __repr__(self) -> str:
        return f"<Tarea(id={self.id}, titulo='{self.titulo}', completada={self.completada})>"
