"""
Ventana Principal de la Aplicacion (QMainWindow) con QStackedWidget.
"""

from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QStackedWidget
from views.components.sidebar import Sidebar
from views.components.topbar import TopBar
from views.dashboard.dashboard_view import DashboardView
from views.clientes.clientes_view import ClientesView
from views.tarifas.tarifas_view import TarifasView
from views.cotizaciones.cotizaciones_view import CotizacionesView
from views.programacion.programacion_view import ProgramacionView
from views.areas_medicas.areas_medicas_view import AreasMedicasView
from views.ordenes_compra.oc_view import OCView
from views.facturacion.facturacion_view import FacturacionView
from views.alertas.alertas_view import AlertasView
from views.historial.historial_view import HistorialView
from views.configuracion.configuracion_view import ConfiguracionView
from workers.alerta_worker import AlertaWorker


class MainWindow(QMainWindow):
    """Ventana contenedora principal del CRM Operativo NE."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("CRM Operativo — Sistema Integral de Gestión de Servicios Médicos NE")
        self.resize(1366, 768)
        self._init_ui()
        self._iniciar_worker_alertas()

    def _init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # 1. Sidebar de Navegacion
        self.sidebar = Sidebar()
        main_layout.addWidget(self.sidebar)

        # 2. Contenedor Derecho (TopBar + StackedWidget)
        right_container = QWidget()
        right_layout = QVBoxLayout(right_container)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(0)

        self.topbar = TopBar()
        right_layout.addWidget(self.topbar)

        # Stack de Modulos
        self.stack = QStackedWidget()
        self.vistas = [
            DashboardView(),        # 0
            ClientesView(),         # 1
            TarifasView(),          # 2
            CotizacionesView(),     # 3
            ProgramacionView(),     # 4
            AreasMedicasView(),     # 5
            OCView(),               # 6
            FacturacionView(),      # 7
            AlertasView(),          # 8
            HistorialView(),        # 9
            ConfiguracionView(),    # 10
        ]

        for vista in self.vistas:
            self.stack.addWidget(vista)

        right_layout.addWidget(self.stack)
        main_layout.addWidget(right_container)

        # Conectar señales del Sidebar
        self.sidebar.modulo_seleccionado.connect(self.stack.setCurrentIndex)

    def _iniciar_worker_alertas(self):
        """Inicia el hilo secundario AlertaWorker para el usuario actual (ID 1)."""
        self.alerta_worker = AlertaWorker(usuario_id=1)
        self.alerta_worker.alertas_actualizadas.connect(self.topbar.alert_bell.actualizar_conteo)
        self.alerta_worker.start()

    def closeEvent(self, event):
        """Asegura la finalizacion limpia del hilo secundario al cerrar la ventana."""
        if hasattr(self, "alerta_worker"):
            self.alerta_worker.detener()
        super().closeEvent(event)
