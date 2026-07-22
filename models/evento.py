"""
Modelo ORM para la entidad Evento.
"""

from datetime import date, time
from typing import List, Optional, TYPE_CHECKING
from sqlalchemy import String, Text, Numeric, Date, Time, Integer, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from core.database import Base
from core.enums import TipoDia

if TYPE_CHECKING:
    from models.cotizacion import Cotizacion
    from models.servicio import Servicio
    from models.ciudad import Ciudad
    from models.extra_evento import ExtraEvento
    from models.programacion import Programacion


class Evento(Base):
    """Representa un servicio individual o evento programado dentro de una cotizacion."""
    __tablename__ = "evento"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    cotizacion_id: Mapped[int] = mapped_column(
        ForeignKey("cotizacion.id", ondelete="CASCADE"), nullable=False
    )
    servicio_id: Mapped[int] = mapped_column(ForeignKey("servicio.id", ondelete="RESTRICT"), nullable=False)
    fecha: Mapped[date] = mapped_column(Date, nullable=False)
    hora_inicio: Mapped[time] = mapped_column(Time, nullable=False)
    hora_fin: Mapped[time] = mapped_column(Time, nullable=False)
    ciudad_id: Mapped[int] = mapped_column(ForeignKey("ciudad.id", ondelete="RESTRICT"), nullable=False)
    direccion: Mapped[str] = mapped_column(String(400), nullable=False)
    contacto: Mapped[str] = mapped_column(String(150), nullable=False)
    telefono: Mapped[str] = mapped_column(String(20), nullable=False)
    observaciones: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Campos calculados automaticamente por el motor de negocio
    tipo_dia: Mapped[TipoDia] = mapped_column(
        SQLEnum(TipoDia, name="tipo_dia_enum"), nullable=False
    )
    horas_diurnas: Mapped[float] = mapped_column(Numeric(6, 2), default=0.0, nullable=False)
    horas_nocturnas: Mapped[float] = mapped_column(Numeric(6, 2), default=0.0, nullable=False)
    valor_horas_diurnas: Mapped[float] = mapped_column(Numeric(14, 2), default=0.0, nullable=False)
    valor_horas_nocturnas: Mapped[float] = mapped_column(Numeric(14, 2), default=0.0, nullable=False)
    valor_extras: Mapped[float] = mapped_column(Numeric(14, 2), default=0.0, nullable=False)
    valor_evento: Mapped[float] = mapped_column(Numeric(14, 2), default=0.0, nullable=False)
    orden: Mapped[int] = mapped_column(Integer, default=1, nullable=False)

    # Relaciones
    cotizacion: Mapped["Cotizacion"] = relationship("Cotizacion", back_populates="eventos")
    servicio: Mapped["Servicio"] = relationship("Servicio", back_populates="eventos")
    ciudad: Mapped["Ciudad"] = relationship("Ciudad", back_populates="eventos")
    extras: Mapped[List["ExtraEvento"]] = relationship(
        "ExtraEvento", back_populates="evento", cascade="all, delete-orphan"
    )
    programaciones: Mapped[List["Programacion"]] = relationship("Programacion", back_populates="evento")

    def __repr__(self) -> str:
        return (
            f"<Evento(id={self.id}, cotizacion_id={self.cotizacion_id}, "
            f"fecha='{self.fecha}', valor_evento={self.valor_evento})>"
        )
