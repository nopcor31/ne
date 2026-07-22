"""
Modelo ORM para la entidad ContactoCliente.
"""

from typing import Optional, TYPE_CHECKING
from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from core.database import Base

if TYPE_CHECKING:
    from models.cliente import Cliente
    from models.cotizacion import Cotizacion


class ContactoCliente(Base):
    """Representa una persona de contacto asociada a un cliente."""
    __tablename__ = "contacto_cliente"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    cliente_id: Mapped[int] = mapped_column(ForeignKey("cliente.id", ondelete="CASCADE"), nullable=False)
    nombre: Mapped[str] = mapped_column(String(150), nullable=False)
    cargo: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    correo: Mapped[Optional[str]] = mapped_column(String(150), nullable=True)
    telefono: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    es_principal: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    activo: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # Relaciones
    cliente: Mapped["Cliente"] = relationship("Cliente", back_populates="contactos")
    cotizaciones: Mapped[list["Cotizacion"]] = relationship("Cotizacion", back_populates="contacto")

    def __repr__(self) -> str:
        return f"<ContactoCliente(id={self.id}, nombre='{self.nombre}', cliente_id={self.cliente_id})>"
