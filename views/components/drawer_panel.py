"""
Componente DrawerPanel — Panel deslizante lateral para detalles sin modal.
"""

from PySide6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Signal


class DrawerPanel(QFrame):
    """Panel lateral desplegable para visualizacion de detalles."""

    cerrado = Signal()

    def __init__(self, titulo: str = "Detalles", parent=None):
        super().__init__(parent)
        self.setStyleSheet("DrawerPanel { background-color: #FFFFFF; border-left: 2px solid #E2E6EC; }")
        self._init_ui(titulo)

    def _init_ui(self, titulo: str):
        self.layout_main = QVBoxLayout(self)
        self.layout_main.setContentsMargins(16, 16, 16, 16)

        # Header con boton cerrar
        header = QHBoxLayout()
        self.lbl_titulo = QLabel(f"<b>{titulo}</b>")
        self.lbl_titulo.setStyleSheet("font-size: 16px; color: #111827;")

        btn_cerrar = QPushButton("✕")
        btn_cerrar.setFixedSize(28, 28)
        btn_cerrar.clicked.connect(self.cerrado.emit)

        header.addWidget(self.lbl_titulo)
        header.addStretch()
        header.addWidget(btn_cerrar)

        self.layout_main.addLayout(header)

    def set_content(self, widget_contenido):
        self.layout_main.addWidget(widget_contenido)
