"""
Componente FilterBar — Barra de filtros dinamicos para tablas.
"""

from PySide6.QtWidgets import QWidget, QHBoxLayout, QComboBox, QLineEdit
from PySide6.QtCore import Signal


class FilterBar(QWidget):
    """Barra de filtros combinada con combo de estados y buscador inline."""

    filtro_cambiado = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_ui()

    def _init_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.combo_estado = QComboBox()
        self.combo_estado.addItem("Todos los Estados")
        self.combo_estado.currentIndexChanged.connect(self.filtro_cambiado.emit)

        self.txt_buscar = QLineEdit()
        self.txt_buscar.setPlaceholderText("Filtrar por texto...")
        self.txt_buscar.textChanged.connect(self.filtro_cambiado.emit)

        layout.addWidget(self.combo_estado)
        layout.addWidget(self.txt_buscar)
        layout.addStretch()
