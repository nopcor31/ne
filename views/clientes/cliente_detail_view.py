"""
Vista Detallada de Cliente (Ficha CRM).
"""

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTabWidget


class ClienteDetailView(QWidget):
    """Vista con pestanas de detalle para un cliente: Info, Contactos, Interacciones, Tareas."""

    def __init__(self, cliente_id: int = None, parent=None):
        super().__init__(parent)
        self.cliente_id = cliente_id
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)

        lbl_titulo = QLabel("<b>Ficha Detallada de Cliente CRM</b>")
        lbl_titulo.setStyleSheet("font-size: 18px;")
        layout.addWidget(lbl_titulo)

        tabs = QTabWidget()
        tabs.addTab(QLabel("Información Básica"), "Información")
        tabs.addTab(QLabel("Contactos"), "Contactos")
        tabs.addTab(QLabel("Interacciones CRM"), "Interacciones")
        tabs.addTab(QLabel("Tareas Pendientes"), "Tareas")
        tabs.addTab(QLabel("Historial"), "Historial")

        layout.addWidget(tabs)
