"""
Modelo ORM para la entidad ExtraEvento.
"""

from typing import TYPE_CHECKING
from sqlalchemy import String, Numeric, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from core.database import Base
from core.enums import TipoExtra

if TYPE_CHECKING:
    from models.evento import Evento


class ExtraEvento(Base):
    """Representa un cargo o costo adicional asociado a un evento especifico."""
    __tablename__ = "extra_evento"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    evento_id: Mapped[int] = mapped_column(
        ForeignKey("evento.id", ondelete="CASCADE"), nullable=False
    )
    tipo: Mapped[TipoExtra] = mapped_column(
        SQLEnum(TipoExtra, name="tipo_extra_enum"), nullable=False
    )
    descripcion: Mapped[str] = mapped_column(String(300), nullable=False)
    valor: Mapped[float] = mapped_column(Numeric(14, 2), nullable=False)

    # Relaciones
    evento: Mapped["Evento"] = relationship("Evento", back_populates="extras")

    def __repr__(self) -> str:
        return f"<ExtraEvento(id={self.id}, tipo='{self.tipo}', valor={self.valor})>"
