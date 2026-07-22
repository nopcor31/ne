"""
Data Transfer Objects (DTO) para la vista del Dashboard.
"""

from dataclasses import dataclass
from typing import List, Dict


@dataclass
class KPICardDTO:
    """DTO para tarjetas de indicadores clave de rendimiento (KPI)."""
    titulo: str
    valor: str
    subtexto: str
    icono: str


@dataclass
class DashboardMetricsDTO:
    """DTO agrupador de metricas globales para el Dashboard."""
    cotizaciones_abiertas: int
    cotizaciones_pendientes_cliente: int
    cotizaciones_pendientes_area_medica: int
    cotizaciones_programadas: int
    facturas_pendientes_pago: int
    total_cotizado_mes: float
    total_facturado_mes: float
    resumen_estados: Dict[str, int]
