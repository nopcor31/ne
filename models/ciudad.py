"""
Modelo ORM para la entidad Ciudad.
"""

from typing import List, TYPE_CHECKING
from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from core.database import Base

if TYPE_CHECKING:
    from models.cliente import Cliente
    from models.tarifa import Tarifa
    from models.evento import Evento


class Ciudad(Base):
    """Representa una ciudad geografica donde se prestan los servicios medicos."""
    __tablename__ = "ciudad"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(150), unique=True, nullable=False, index=True)
    departamento: Mapped[str] = mapped_column(String(100), nullable=False)
    activo: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # Relaciones
    clientes: Mapped[List["Cliente"]] = relationship("Cliente", back_populates="ciudad")
    tarifas: Mapped[List["Tarifa"]] = relationship("Tarifa", back_populates="ciudad")
    eventos: Mapped[List["Evento"]] = relationship("Evento", back_populates="ciudad")

    def __repr__(self) -> str:
        return f"<Ciudad(id={self.id}, nombre='{self.nombre}', departamento='{self.departamento}')>"
