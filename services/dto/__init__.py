"""
Paquete de Data Transfer Objects (DTO) para la capa de servicios.
"""

from services.dto.cliente_dto import ClienteDTO, ContactoDTO
from services.dto.evento_dto import EventoDTO, ExtraEventoDTO
from services.dto.cotizacion_dto import CotizacionDTO
from services.dto.tarifa_dto import TarifaDTO
from services.dto.dashboard_dto import KPICardDTO, DashboardMetricsDTO

__all__ = [
    "ClienteDTO",
    "ContactoDTO",
    "EventoDTO",
    "ExtraEventoDTO",
    "CotizacionDTO",
    "TarifaDTO",
    "KPICardDTO",
    "DashboardMetricsDTO",
]
