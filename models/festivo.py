"""
Modelo ORM para la entidad Festivo.
"""

from datetime import date
from sqlalchemy import String, Date, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column
from core.database import Base
from core.enums import OrigenFestivo


class Festivo(Base):
    """Representa un dia festivo legal registrado en el calendario laboral."""
    __tablename__ = "festivo"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    fecha: Mapped[date] = mapped_column(Date, unique=True, nullable=False, index=True)
    nombre: Mapped[str] = mapped_column(String(200), nullable=False)
    origen: Mapped[OrigenFestivo] = mapped_column(
        SQLEnum(OrigenFestivo, name="origen_festivo_enum"), default=OrigenFestivo.LIBRERIA, nullable=False
    )

    def __repr__(self) -> str:
        return f"<Festivo(id={self.id}, fecha='{self.fecha}', nombre='{self.nombre}')>"
