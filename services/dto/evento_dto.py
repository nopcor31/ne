"""
Data Transfer Objects (DTO) para la entidad Evento y ExtraEvento.
"""

from dataclasses import dataclass
from datetime import date, time
from typing import Optional, List
from core.enums import TipoDia, TipoExtra


@dataclass
class ExtraEventoDTO:
    """DTO para transferencia de un extra de evento."""
    id: Optional[int]
    tipo: TipoExtra
    descripcion: str
    valor: float


@dataclass
class EventoDTO:
    """DTO para transferencia de informacion completa de un evento."""
    id: Optional[int]
    cotizacion_id: Optional[int]
    servicio_id: int
    servicio_nombre: Optional[str]
    fecha: date
    hora_inicio: time
    hora_fin: time
    ciudad_id: int
    ciudad_nombre: Optional[str]
    direccion: str
    contacto: str
    telefono: str
    observaciones: Optional[str]
    tipo_dia: TipoDia
    horas_diurnas: float
    horas_nocturnas: float
    valor_horas_diurnas: float
    valor_horas_nocturnas: float
    valor_extras: float
    valor_evento: float
    orden: int
    extras: List[ExtraEventoDTO]
