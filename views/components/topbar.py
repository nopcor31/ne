"""
Componente Topbar — Encabezado superior con busqueda y notificaciones.
"""

from PySide6.QtWidgets import QWidget, QHBoxLayout, QLineEdit, QLabel, QPushButton
from PySide6.QtCore import Signal
from views.components.alert_bell import AlertBell


class TopBar(QWidget):
    """Barra superior con buscador global, icono de alertas y perfil de usuario."""

    # Señal emitida al escribir en la busqueda global
    busqueda_cambiada = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("topbar")
        self._init_ui()

    def _init_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 8, 16, 8)

        # Buscador global
        self.txt_buscar = QLineEdit()
        self.txt_buscar.setPlaceholderText("🔍 Buscar clientes, cotizaciones, NIT...")
        self.txt_buscar.textChanged.connect(self.busqueda_cambiada.emit)
        layout.addWidget(self.txt_buscar, stretch=2)

        layout.addStretch(stretch=1)

        # Boton Campanita de Alertas
        self.alert_bell = AlertBell()
        layout.addWidget(self.alert_bell)

        # Perfil del Usuario
        lbl_usuario = QLabel("👤 Admin (Ejecutivo Comercial)")
        lbl_usuario.setStyleSheet("font-weight: 500; color: #374151; padding-left: 12px;")
        layout.addWidget(lbl_usuario)
