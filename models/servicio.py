"""
Modelo ORM para la entidad Servicio.
"""

from typing import List, TYPE_CHECKING
from sqlalchemy import String, Boolean, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from core.database import Base
from core.enums import TipoServicio

if TYPE_CHECKING:
    from models.tarifa import Tarifa
    from models.evento import Evento


class Servicio(Base):
    """Representa un tipo de servicio medico o ambulatorio en el catalogo."""
    __tablename__ = "servicio"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    codigo: Mapped[str] = mapped_column(String(30), unique=True, nullable=False, index=True)
    nombre: Mapped[str] = mapped_column(String(200), nullable=False)
    tipo: Mapped[TipoServicio] = mapped_column(
        SQLEnum(TipoServicio, name="tipo_servicio_enum"), nullable=False
    )
    activo: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # Relaciones
    tarifas: Mapped[List["Tarifa"]] = relationship("Tarifa", back_populates="servicio")
    eventos: Mapped[List["Evento"]] = relationship("Evento", back_populates="servicio")

    def __repr__(self) -> str:
        return f"<Servicio(id={self.id}, codigo='{self.codigo}', nombre='{self.nombre}')>"
