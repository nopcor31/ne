"""
Vista de Detalle de Expediente de Cotizacion.
"""

from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from views.components.progress_steps import ProgressSteps
from views.components.modern_table import ModernTable


class CotizacionDetailView(QWidget):
    """Vista completa del expediente de cotizacion: resumen, pasos, eventos y PDF."""

    def __init__(self, cotizacion_id: int = None, parent=None):
        super().__init__(parent)
        self.cotizacion_id = cotizacion_id
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)

        # Progress Steps bar
        self.steps = ProgressSteps()
        layout.addWidget(self.steps)

        # Acciones
        acciones = QHBoxLayout()
        btn_pdf = QPushButton("🖨 Ver / Generar PDF")
        btn_email = QPushButton("📧 Enviar por Outlook")
        acciones.addStretch()
        acciones.addWidget(btn_pdf)
        acciones.addWidget(btn_email)
        layout.addLayout(acciones)

        # Tabla de Eventos
        lbl_ev = QLabel("<b>Eventos de Servicio</b>")
        lbl_ev.setStyleSheet("font-size: 16px; padding-top: 12px;")
        layout.addWidget(lbl_ev)

        self.tabla_eventos = ModernTable()
        self.tabla_eventos.setColumnCount(5)
        self.tabla_eventos.setHorizontalHeaderLabels(["Servicio", "Fecha", "Ciudad", "Horas (D/N)", "Total Evento"])
        layout.addWidget(self.tabla_eventos)
