"""
Modelo ORM para la entidad Programacion.
"""

from datetime import date, time
from typing import Optional, TYPE_CHECKING
from sqlalchemy import String, Text, Date, Time, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from core.database import Base
from core.enums import EstadoProgramacion

if TYPE_CHECKING:
    from models.cotizacion import Cotizacion
    from models.evento import Evento


class Programacion(Base):
    """Representa la asignacion en agenda de un evento de servicio aprobado."""
    __tablename__ = "programacion"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    cotizacion_id: Mapped[int] = mapped_column(
        ForeignKey("cotizacion.id", ondelete="CASCADE"), nullable=False
    )
    evento_id: Mapped[int] = mapped_column(
        ForeignKey("evento.id", ondelete="CASCADE"), nullable=False
    )
    fecha_programada: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    hora_inicio: Mapped[time] = mapped_column(Time, nullable=False)
    hora_fin: Mapped[time] = mapped_column(Time, nullable=False)
    recurso_asignado: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    notas: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    outlook_event_id: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    estado: Mapped[EstadoProgramacion] = mapped_column(
        SQLEnum(EstadoProgramacion, name="estado_programacion_enum"),
        default=EstadoProgramacion.PENDIENTE,
        nullable=False
    )

    # Relaciones
    cotizacion: Mapped["Cotizacion"] = relationship("Cotizacion", back_populates="programaciones")
    evento: Mapped["Evento"] = relationship("Evento", back_populates="programaciones")

    def __repr__(self) -> str:
        return (
            f"<Programacion(id={self.id}, fecha='{self.fecha_programada}', "
            f"recurso='{self.recurso_asignado}', estado='{self.estado}')>"
        )
