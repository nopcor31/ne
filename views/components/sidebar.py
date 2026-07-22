"""
Componente Sidebar — Navegacion Lateral Colapsable PySide6.
"""

from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QButtonGroup
from PySide6.QtCore import Signal, Qt


class Sidebar(QWidget):
    """Barra de navegacion lateral con soporte para colapsado y seleccion activa."""

    # Señal emitida al seleccionar un modulo (indice del stacked widget)
    modulo_seleccionado = Signal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("sidebar")
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 16, 12, 16)
        layout.setSpacing(8)

        # Header con Logo y Nombre
        lbl_logo = QLabel("<b>NE</b> SERVICIOS")
        lbl_logo.setStyleSheet("font-size: 16px; font-weight: bold; color: #1B6FD8; padding-bottom: 12px;")
        layout.addWidget(lbl_logo)

        # Grupo de botones de navegacion
        self.button_group = QButtonGroup(self)
        self.button_group.setExclusive(True)

        modulos = [
            ("📊 Dashboard", 0),
            ("👥 Clientes CRM", 1),
            ("💲 Tarifas", 2),
            ("📋 Cotizaciones", 3),
            ("📅 Programación", 4),
            ("🏥 Áreas Médicas", 5),
            ("📦 Órdenes de Compra", 6),
            ("🧾 Facturación", 7),
            ("🔔 Alertas", 8),
            ("📖 Historial", 9),
            ("⚙ Configuración", 10),
        ]

        for idx, (texto, modulo_idx) in enumerate(modulos):
            btn = QPushButton(texto)
            btn.setCheckable(True)
            if idx == 0:
                btn.setChecked(True)
            self.button_group.addButton(btn, modulo_idx)
            layout.addWidget(btn)

        self.button_group.idClicked.connect(self._on_modulo_clicked)
        layout.addStretch()

    def _on_modulo_clicked(self, modulo_idx: int):
        self.modulo_seleccionado.emit(modulo_idx)
