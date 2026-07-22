"""
Data Transfer Objects (DTO) para la entidad Tarifa.
"""

from dataclasses import dataclass
from datetime import date
from typing import Optional
from core.enums import TipoDia, TipoHorario


@dataclass
class TarifaDTO:
    """DTO para transferencia de tarifas."""
    id: Optional[int]
    ciudad_id: int
    ciudad_nombre: Optional[str]
    servicio_id: int
    servicio_nombre: Optional[str]
    tipo_dia: TipoDia
    tipo_horario: TipoHorario
    cliente_id: Optional[int]
    cliente_nombre: Optional[str]
    valor_hora: float
    vigente_desde: date
    vigente_hasta: Optional[date]
    activo: bool
