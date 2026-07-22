"""
Modelo ORM para la entidad Usuario.
"""

from datetime import datetime
from typing import List, TYPE_CHECKING
from sqlalchemy import String, Boolean, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from core.database import Base

if TYPE_CHECKING:
    from models.cliente import Cliente
    from models.cotizacion import Cotizacion
    from models.tarea import Tarea
    from models.historial_actividad import HistorialActividad


class Usuario(Base):
    """Representa un usuario dentro del sistema CRM Operativo."""
    __tablename__ = "usuario"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(150), unique=True, nullable=False, index=True)
    activo: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    fecha_creacion: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), nullable=False
    )

    # Relaciones
    clientes_creados: Mapped[List["Cliente"]] = relationship(
        "Cliente", back_populates="usuario_creador", foreign_keys="Cliente.usuario_creador_id"
    )
    cotizaciones_creadas: Mapped[List["Cotizacion"]] = relationship(
        "Cotizacion", back_populates="usuario_creador", foreign_keys="Cotizacion.usuario_creador_id"
    )
    cotizaciones_asignadas: Mapped[List["Cotizacion"]] = relationship(
        "Cotizacion", back_populates="usuario_asignado", foreign_keys="Cotizacion.usuario_asignado_id"
    )
    tareas_asignadas: Mapped[List["Tarea"]] = relationship(
        "Tarea", back_populates="usuario_asignado", foreign_keys="Tarea.usuario_asignado_id"
    )
    actividades_historial: Mapped[List["HistorialActividad"]] = relationship(
        "HistorialActividad", back_populates="usuario"
    )

    def __repr__(self) -> str:
        return f"<Usuario(id={self.id}, nombre='{self.nombre}', email='{self.email}')>"
