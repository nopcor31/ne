"""
Servicio para agregacion de metricas y KPIs del Dashboard gerencial.
"""

from typing import Dict
from sqlalchemy.orm import Session
from sqlalchemy import select, func
from models.cotizacion import Cotizacion
from models.factura import Factura
from repositories.cotizacion_repository import CotizacionRepository
from repositories.factura_repository import FacturaRepository
from services.dto.dashboard_dto import DashboardMetricsDTO
from core.enums import EstadoCotizacion, EstadoFactura


class DashboardService:
    """Servicio de calculo y consolidacion de KPIs para la vista Dashboard."""

    def __init__(self, session: Session):
        self.session = session
        self.cotizacion_repo = CotizacionRepository(session)
        self.factura_repo = FacturaRepository(session)

    def obtener_metricas(self) -> DashboardMetricsDTO:
        """Calcula y retorna los indicadores clave para la pantalla principal."""
        # Cotizaciones por estado
        resumen_estados: Dict[str, int] = {}
        for estado in EstadoCotizacion:
            stmt = select(func.count(Cotizacion.id)).where(Cotizacion.estado == estado)
            cant = self.session.scalar(stmt) or 0
            resumen_estados[estado.value] = cant

        # Totales financieros acumulados
        stmt_total_cot = select(func.sum(Cotizacion.valor_total)).where(
            Cotizacion.estado != EstadoCotizacion.RECHAZADA_CLIENTE
        )
        total_cotizado = float(self.session.scalar(stmt_total_cot) or 0.0)

        stmt_total_fac = select(func.sum(Factura.valor_facturado)).where(
            Factura.estado == EstadoFactura.PAGADA
        )
        total_facturado = float(self.session.scalar(stmt_total_fac) or 0.0)

        # Cantidad de facturas pendientes de pago
        stmt_fac_pend = select(func.count(Factura.id)).where(
            Factura.estado == EstadoFactura.FACTURADA
        )
        facturas_pendientes = self.session.scalar(stmt_fac_pend) or 0

        return DashboardMetricsDTO(
            cotizaciones_abiertas=resumen_estados.get(EstadoCotizacion.COTIZADA.value, 0) +
                                  resumen_estados.get(EstadoCotizacion.BORRADOR.value, 0),
            cotizaciones_pendientes_cliente=resumen_estados.get(EstadoCotizacion.ENVIADA_CLIENTE.value, 0),
            cotizaciones_pendientes_area_medica=resumen_estados.get(EstadoCotizacion.PENDIENTE_AREA_MEDICA.value, 0),
            cotizaciones_programadas=resumen_estados.get(EstadoCotizacion.PROGRAMADA.value, 0),
            facturas_pendientes_pago=facturas_pendientes,
            total_cotizado_mes=total_cotizado,
            total_facturado_mes=total_facturado,
            resumen_estados=resumen_estados
        )
