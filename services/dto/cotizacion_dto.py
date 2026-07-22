"""
Data Transfer Objects (DTO) para la entidad Cotizacion.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List
from core.enums import EstadoCotizacion
from services.dto.evento_dto import EventoDTO


@dataclass
class CotizacionDTO:
    """DTO para transferencia de informacion de expediente de cotizacion."""
    id: Optional[int]
    numero_cotizacion: str
    cliente_id: int
    cliente_nombre: Optional[str]
    contacto_id: Optional[int]
    contacto_nombre: Optional[str]
    estado: EstadoCotizacion
    usuario_creador_id: int
    usuario_creador_nombre: Optional[str]
    fecha_creacion: datetime
    fecha_enviada_cliente: Optional[datetime]
    fecha_respuesta_cliente: Optional[datetime]
    valor_subtotal: float
    valor_extras: float
    valor_total: float
    observaciones: Optional[str]
    condiciones_comerciales: Optional[str]
    pdf_path: Optional[str]
    eventos: List[EventoDTO]
