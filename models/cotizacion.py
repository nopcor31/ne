"""
Modelo ORM para la entidad Cotizacion.
"""

from datetime import datetime
from typing import List, Optional, TYPE_CHECKING
from sqlalchemy import String, Text, Numeric, DateTime, ForeignKey, Enum as SQLEnum, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from core.database import Base
from core.enums import EstadoCotizacion

if TYPE_CHECKING:
    from models.cliente import Cliente
    from models.contacto_cliente import ContactoCliente
    from models.usuario import Usuario
    from models.evento import Evento
    from models.interaccion_crm import InteraccionCRM
    from models.tarea import Tarea
    from models.envio_area_medica import EnvioAreaMedica
    from models.programacion import Programacion
    from models.orden_compra import OrdenCompra
    from models.factura import Factura


class Cotizacion(Base):
    """Representa el expediente principal de cotizacion y su ciclo de vida comercial."""
    __tablename__ = "cotizacion"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    numero_cotizacion: Mapped[str] = mapped_column(String(20), unique=True, nullable=False, index=True)
    cliente_id: Mapped[int] = mapped_column(ForeignKey("cliente.id", ondelete="RESTRICT"), nullable=False)
    contacto_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("contacto_cliente.id", ondelete="SET NULL"), nullable=True
    )
    estado: Mapped[EstadoCotizacion] = mapped_column(
        SQLEnum(EstadoCotizacion, name="estado_cotizacion_enum"),
        default=EstadoCotizacion.BORRADOR,
        nullable=False,
        index=True
    )
    usuario_creador_id: Mapped[int] = mapped_column(
        ForeignKey("usuario.id", ondelete="RESTRICT"), nullable=False
    )
    usuario_asignado_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("usuario.id", ondelete="SET NULL"), nullable=True
    )

    # Fechas del flujo de estados
    fecha_creacion: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), nullable=False
    )
    fecha_enviada_cliente: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    fecha_respuesta_cliente: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    fecha_enviada_area: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    fecha_aprobacion_area: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    fecha_programacion: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    fecha_oc_solicitada: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    fecha_oc_recibida: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    fecha_facturacion: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    fecha_pago: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    # Totales Financieros
    valor_subtotal: Mapped[float] = mapped_column(Numeric(14, 2), default=0.0, nullable=False)
    valor_extras: Mapped[float] = mapped_column(Numeric(14, 2), default=0.0, nullable=False)
    valor_total: Mapped[float] = mapped_column(Numeric(14, 2), default=0.0, nullable=False)

    observaciones: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    condiciones_comerciales: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    pdf_path: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)

    # Relaciones
    cliente: Mapped["Cliente"] = relationship("Cliente", back_populates="cotizaciones")
    contacto: Mapped[Optional["ContactoCliente"]] = relationship("ContactoCliente", back_populates="cotizaciones")
    usuario_creador: Mapped["Usuario"] = relationship(
        "Usuario", back_populates="cotizaciones_creadas", foreign_keys=[usuario_creador_id]
    )
    usuario_asignado: Mapped[Optional["Usuario"]] = relationship(
        "Usuario", back_populates="cotizaciones_asignadas", foreign_keys=[usuario_asignado_id]
    )

    eventos: Mapped[List["Evento"]] = relationship(
        "Evento", back_populates="cotizacion", cascade="all, delete-orphan", order_by="Evento.orden"
    )
    interacciones: Mapped[List["InteraccionCRM"]] = relationship("InteraccionCRM", back_populates="cotizacion")
    tareas: Mapped[List["Tarea"]] = relationship("Tarea", back_populates="cotizacion")
    envios_area_medica: Mapped[List["EnvioAreaMedica"]] = relationship("EnvioAreaMedica", back_populates="cotizacion")
    programaciones: Mapped[List["Programacion"]] = relationship("Programacion", back_populates="cotizacion")
    ordenes_compra: Mapped[List["OrdenCompra"]] = relationship("OrdenCompra", back_populates="cotizacion")
    facturas: Mapped[List["Factura"]] = relationship("Factura", back_populates="cotizacion")

    def __repr__(self) -> str:
        return f"<Cotizacion(id={self.id}, numero='{self.numero_cotizacion}', estado='{self.estado}')>"
