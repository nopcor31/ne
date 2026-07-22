"""
Modelo ORM para la entidad Configuracion.
"""

from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column
from core.database import Base


class Configuracion(Base):
    """Tabla clave-valor para parametros dinámicos de configuracion del sistema."""
    __tablename__ = "configuracion"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    clave: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    valor: Mapped[str] = mapped_column(Text, nullable=False)
    descripcion: Mapped[str] = mapped_column(String(300), nullable=False)

    def __repr__(self) -> str:
        return f"<Configuracion(clave='{self.clave}', valor='{self.valor}')>"
