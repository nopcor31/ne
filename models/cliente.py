"""
Modelo ORM para la entidad Cliente.
"""

from datetime import datetime
from typing import List, Optional, TYPE_CHECKING
from sqlalchemy import String, Boolean, DateTime, Text, ForeignKey, Enum as SQLEnum, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from core.database import Base
from core.enums import TipoCliente

if TYPE_CHECKING:
    from models.usuario import Usuario
    from models.ciudad import Ciudad
    from models.contacto_cliente import ContactoCliente
    from models.interaccion_crm import InteraccionCRM
    from models.tarea import Tarea
    from models.tarifa import Tarifa
    from models.cotizacion import Cotizacion


class Cliente(Base):
    """Representa un cliente de la organizacion en el CRM."""
    __tablename__ = "cliente"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    empresa: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    nit: Mapped[str] = mapped_column(String(20), unique=True, nullable=False, index=True)
    correo_principal: Mapped[str] = mapped_column(String(150), nullable=False)
    telefono_principal: Mapped[str] = mapped_column(String(20), nullable=False)
    tipo_cliente: Mapped[TipoCliente] = mapped_column(
        SQLEnum(TipoCliente, name="tipo_cliente_enum"), default=TipoCliente.NORMAL, nullable=False
    )
    sector: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    ciudad_id: Mapped[int] = mapped_column(ForeignKey("ciudad.id", ondelete="RESTRICT"), nullable=False)
    direccion: Mapped[Optional[str]] = mapped_column(String(300), nullable=True)
    sitio_web: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    observaciones: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    activo: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    fecha_creacion: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), nullable=False
    )
    usuario_creador_id: Mapped[int] = mapped_column(
        ForeignKey("usuario.id", ondelete="RESTRICT"), nullable=False
    )

    # Relaciones
    ciudad: Mapped["Ciudad"] = relationship("Ciudad", back_populates="clientes")
    usuario_creador: Mapped["Usuario"] = relationship(
        "Usuario", back_populates="clientes_creados", foreign_keys=[usuario_creador_id]
    )
    contactos: Mapped[List["ContactoCliente"]] = relationship(
        "ContactoCliente", back_populates="cliente", cascade="all, delete-orphan"
    )
    interacciones: Mapped[List["InteraccionCRM"]] = relationship(
        "InteraccionCRM", back_populates="cliente", cascade="all, delete-orphan"
    )
    tareas: Mapped[List["Tarea"]] = relationship("Tarea", back_populates="cliente")
    tarifas_especiales: Mapped[List["Tarifa"]] = relationship("Tarifa", back_populates="cliente")
    cotizaciones: Mapped[List["Cotizacion"]] = relationship("Cotizacion", back_populates="cliente")

    def __repr__(self) -> str:
        return f"<Cliente(id={self.id}, empresa='{self.empresa}', nit='{self.nit}', tipo='{self.tipo_cliente}')>"
