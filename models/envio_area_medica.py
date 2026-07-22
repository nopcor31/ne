"""
Modelo ORM para la entidad EnvioAreaMedica.
"""

from datetime import datetime
from typing import Optional, TYPE_CHECKING
from sqlalchemy import Text, Boolean, DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from core.database import Base

if TYPE_CHECKING:
    from models.cotizacion import Cotizacion
    from models.area_medica import AreaMedica
    from models.usuario import Usuario


class EnvioAreaMedica(Base):
    """Registro del envio de una cotizacion a un area medica para revision tecnica."""
    __tablename__ = "envio_area_medica"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    cotizacion_id: Mapped[int] = mapped_column(
        ForeignKey("cotizacion.id", ondelete="CASCADE"), nullable=False
    )
    area_medica_id: Mapped[int] = mapped_column(
        ForeignKey("area_medica.id", ondelete="RESTRICT"), nullable=False
    )
    fecha_envio: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), nullable=False
    )
    usuario_envio_id: Mapped[int] = mapped_column(
        ForeignKey("usuario.id", ondelete="RESTRICT"), nullable=False
    )
    fecha_respuesta: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    aprobado: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)  # None = Pendiente
    observaciones_respuesta: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Relaciones
    cotizacion: Mapped["Cotizacion"] = relationship("Cotizacion", back_populates="envios_area_medica")
    area_medica: Mapped["AreaMedica"] = relationship("AreaMedica", back_populates="envios")
    usuario_envio: Mapped["Usuario"] = relationship("Usuario")

    def __repr__(self) -> str:
        return (
            f"<EnvioAreaMedica(id={self.id}, cotizacion_id={self.cotizacion_id}, "
            f"area_id={self.area_medica_id}, aprobado={self.aprobado})>"
        )
