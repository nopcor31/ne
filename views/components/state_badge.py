"""
Componente StateBadge — Pill de color segun el estado de la cotizacion.
"""

from PySide6.QtWidgets import QLabel
from core.enums import EstadoCotizacion


class StateBadge(QLabel):
    """Badge/Etiqueta visual con color dinamico segun estado."""

    ESTILO_COLORES = {
        EstadoCotizacion.BORRADOR: ("#F3F4F6", "#4B5563"),
        EstadoCotizacion.COTIZADA: ("#EFF6FF", "#1D4ED8"),
        EstadoCotizacion.ENVIADA_CLIENTE: ("#F5F3FF", "#6D28D9"),
        EstadoCotizacion.ACEPTADA_CLIENTE: ("#ECFDF5", "#047857"),
        EstadoCotizacion.RECHAZADA_CLIENTE: ("#FEF2F2", "#B91C1C"),
        EstadoCotizacion.PENDIENTE_AREA_MEDICA: ("#FFFBEB", "#B45309"),
        EstadoCotizacion.PROGRAMADA: ("#ECFEFF", "#0E7490"),
        EstadoCotizacion.OC_SOLICITADA: ("#EEF2FF", "#4338CA"),
        EstadoCotizacion.OC_RECIBIDA: ("#F0FDF4", "#15803D"),
        EstadoCotizacion.PENDIENTE_FACTURACION: ("#FEF9C3", "#854D0E"),
        EstadoCotizacion.FACTURADA: ("#F7FEE7", "#4D7C0F"),
        EstadoCotizacion.PAGADA: ("#DCFCE7", "#15803D"),
        EstadoCotizacion.CERRADA: ("#E5E7EB", "#374151"),
    }

    def __init__(self, estado: EstadoCotizacion, parent=None):
        super().__init__(estado.value if estado else "", parent)
        self._aplicar_estilo(estado)

    def _aplicar_estilo(self, estado: EstadoCotizacion):
        bg, text = self.ESTILO_COLORES.get(estado, ("#E5E7EB", "#374151"))
        self.setStyleSheet(
            f"background-color: {bg}; color: {text}; border-radius: 12px; "
            "padding: 4px 10px; font-weight: 600; font-size: 11px;"
        )
