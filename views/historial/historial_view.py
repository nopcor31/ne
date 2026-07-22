"""
Vista de Bitacora e Historial Auditor de Actividades y Trazabilidad.
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QComboBox, QMessageBox
)
from controllers.historial_controller import HistorialController
from views.components.timeline_widget import TimelineWidget


class HistorialView(QWidget):
    """Vista de auditoria global con timeline cronológico de trazabilidad."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.controller = HistorialController()
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(16)

        header = QHBoxLayout()
        lbl_titulo = QLabel("<b>Bitácora e Historial de Auditoría</b>")
        lbl_titulo.setStyleSheet("font-size: 20px; color: #0F172A;")

        btn_refrescar = QPushButton("🔄 Actualizar Bitácora")
        btn_refrescar.setObjectName("btnSecondary")
        btn_refrescar.clicked.connect(self.cargar_historial)

        header.addWidget(lbl_titulo)
        header.addStretch()
        header.addWidget(btn_refrescar)

        layout.addLayout(header)

        self.timeline = TimelineWidget()
        layout.addWidget(self.timeline)

        self.cargar_historial()

    def cargar_historial(self):
        try:
            eventos = self.controller.obtener_historial_global(limite=50)
            self.timeline.cargar_eventos(eventos)
        except Exception as e:
            pass
