"""
Modelo ORM para la entidad AreaMedica.
"""

from typing import List, Optional, TYPE_CHECKING
from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from core.database import Base

if TYPE_CHECKING:
    from models.envio_area_medica import EnvioAreaMedica


class AreaMedica(Base):
    """Representa un area medica o departamento medico evaluador de servicios."""
    __tablename__ = "area_medica"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(200), nullable=False)
    correo_contacto: Mapped[str] = mapped_column(String(150), nullable=False)
    telefono: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    responsable: Mapped[Optional[str]] = mapped_column(String(150), nullable=True)
    activo: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # Relaciones
    envios: Mapped[List["EnvioAreaMedica"]] = relationship("EnvioAreaMedica", back_populates="area_medica")

    def __repr__(self) -> str:
        return f"<AreaMedica(id={self.id}, nombre='{self.nombre}', correo='{self.correo_contacto}')>"
