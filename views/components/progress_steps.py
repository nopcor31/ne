"""
Componente ProgressSteps — Indicador visual de avance del pipeline comercial.
"""

from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel
from core.enums import EstadoCotizacion


class ProgressSteps(QWidget):
    """Barra de progreso visual por fases del expediente de cotizacion."""

    PASOS_PRINCIPALES = [
        (EstadoCotizacion.BORRADOR, "1. Borrador"),
        (EstadoCotizacion.COTIZADA, "2. Cotizada"),
        (EstadoCotizacion.ENVIADA_CLIENTE, "3. Enviada"),
        (EstadoCotizacion.ACEPTADA_CLIENTE, "4. Aceptada"),
        (EstadoCotizacion.PROGRAMADA, "5. Programada"),
        (EstadoCotizacion.FACTURADA, "6. Facturada"),
        (EstadoCotizacion.PAGADA, "7. Pagada"),
    ]

    def __init__(self, estado_actual: EstadoCotizacion = EstadoCotizacion.BORRADOR, parent=None):
        super().__init__(parent)
        self._init_ui(estado_actual)

    def _init_ui(self, estado_actual: EstadoCotizacion):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)

        alcanzado = True
        for estado_step, etiqueta in self.PASOS_PRINCIPALES:
            lbl = QLabel(etiqueta)
            if alcanzado:
                lbl.setStyleSheet("background-color: #E8F0FD; color: #1B6FD8; padding: 4px 8px; border-radius: 4px; font-weight: bold; font-size: 11px;")
            else:
                lbl.setStyleSheet("background-color: #F4F6FA; color: #9CA3AF; padding: 4px 8px; border-radius: 4px; font-size: 11px;")

            if estado_step == estado_actual:
                alcanzado = False

            layout.addWidget(lbl)
