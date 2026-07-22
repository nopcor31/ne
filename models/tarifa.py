"""
Modelo ORM para la entidad Tarifa.
"""

from datetime import date
from typing import Optional, TYPE_CHECKING
from sqlalchemy import Numeric, Boolean, Date, ForeignKey, Enum as SQLEnum, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from core.database import Base
from core.enums import TipoDia, TipoHorario

if TYPE_CHECKING:
    from models.ciudad import Ciudad
    from models.servicio import Servicio
    from models.cliente import Cliente


class Tarifa(Base):
    """Representa la tarifa por hora aplicable a un servicio en una ciudad y horario especifico."""
    __tablename__ = "tarifa"
    __table_args__ = (
        UniqueConstraint(
            "ciudad_id", "servicio_id", "tipo_dia", "tipo_horario", "cliente_id", "vigente_desde",
            name="uq_tarifa_combinacion_vigencia"
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    ciudad_id: Mapped[int] = mapped_column(ForeignKey("ciudad.id", ondelete="RESTRICT"), nullable=False)
    servicio_id: Mapped[int] = mapped_column(ForeignKey("servicio.id", ondelete="RESTRICT"), nullable=False)
    tipo_dia: Mapped[TipoDia] = mapped_column(
        SQLEnum(TipoDia, name="tipo_dia_enum"), nullable=False
    )
    tipo_horario: Mapped[TipoHorario] = mapped_column(
        SQLEnum(TipoHorario, name="tipo_horario_enum"), nullable=False
    )
    cliente_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("cliente.id", ondelete="CASCADE"), nullable=True, index=True
    )
    valor_hora: Mapped[float] = mapped_column(Numeric(14, 2), nullable=False)
    vigente_desde: Mapped[date] = mapped_column(Date, nullable=False)
    vigente_hasta: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    activo: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # Relaciones
    ciudad: Mapped["Ciudad"] = relationship("Ciudad", back_populates="tarifas")
    servicio: Mapped["Servicio"] = relationship("Servicio", back_populates="tarifas")
    cliente: Mapped[Optional["Cliente"]] = relationship("Cliente", back_populates="tarifas_especiales")

    def __repr__(self) -> str:
        return (
            f"<Tarifa(id={self.id}, ciudad_id={self.ciudad_id}, servicio_id={self.servicio_id}, "
            f"valor_hora={self.valor_hora}, cliente_id={self.cliente_id})>"
        )
