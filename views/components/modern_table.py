"""
Componente ModernTable — QTableWidget estilizado para listados.
"""

from PySide6.QtWidgets import QTableWidget, QHeaderView, QAbstractItemView


class ModernTable(QTableWidget):
    """Tabla estilizada con configuracion por defecto para listas empresariales."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setAlternatingRowColors(True)
        self.setSortingEnabled(True)
        self.verticalHeader().setVisible(False)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
