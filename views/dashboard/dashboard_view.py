"""
Vista principal del Dashboard Gerencial.
"""

from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QGridLayout
from controllers.dashboard_controller import DashboardController
from views.components.kpi_card import KPICard
from views.components.timeline_widget import TimelineWidget


class DashboardView(QWidget):
    """Vista de resumen con indicadores KPI y feed de actividad reciente."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.controller = DashboardController()
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(16)

        lbl_titulo = QLabel("<b>Dashboard Operativo</b>")
        lbl_titulo.setStyleSheet("font-size: 20px; color: #111827;")
        layout.addWidget(lbl_titulo)

        # Grilla de Tarjetas KPI
        grid_kpi = QGridLayout()
        grid_kpi.setSpacing(12)

        self.kpi_abiertas = KPICard("Cotizaciones Abiertas", "0", "Borradores y Cotizadas", "📋")
        self.kpi_enviadas = KPICard("Pendientes Cliente", "0", "Enviadas a Cliente", "⏳")
        self.kpi_area_medica = KPICard("Pendientes Área Médica", "0", "En revisión técnica", "🏥")
        self.kpi_programadas = KPICard("Servicios Programados", "0", "Confirmados en agenda", "📅")

        grid_kpi.addWidget(self.kpi_abiertas, 0, 0)
        grid_kpi.addWidget(self.kpi_enviadas, 0, 1)
        grid_kpi.addWidget(self.kpi_area_medica, 0, 2)
        grid_kpi.addWidget(self.kpi_programadas, 0, 3)

        layout.addLayout(grid_kpi)

        # Timeline de Actividad Reciente
        lbl_act = QLabel("<b>Actividad Reciente</b>")
        lbl_act.setStyleSheet("font-size: 16px; color: #111827; padding-top: 12px;")
        layout.addWidget(lbl_act)

        self.timeline = TimelineWidget()
        layout.addWidget(self.timeline)

        self.cargar_datos()

    def cargar_datos(self):
        try:
            metricas = self.controller.obtener_metricas_dashboard()
            self.kpi_abiertas.actualizar_valor(str(metricas.cotizaciones_abiertas))
            self.kpi_enviadas.actualizar_valor(str(metricas.cotizaciones_pendientes_cliente))
            self.kpi_area_medica.actualizar_valor(str(metricas.cotizaciones_pendientes_area_medica))
            self.kpi_programadas.actualizar_valor(str(metricas.cotizaciones_programadas))

            actividad = self.controller.obtener_actividad_reciente(15)
            self.timeline.cargar_eventos(actividad)
        except Exception:
            pass
