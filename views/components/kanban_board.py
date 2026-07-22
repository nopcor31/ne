"""
Componente KanbanBoard — Tablero Kanban organizado por columnas de estado.
"""

from typing import List, Dict
from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QScrollArea
from PySide6.QtCore import Signal
from services.dto.cotizacion_dto import CotizacionDTO
from views.components.kanban_card import KanbanCard
from core.enums import EstadoCotizacion


class KanbanBoard(QWidget):
    """Tablero Kanban con columnas agrupadas por estados del pipeline comercial."""

    cotizacion_seleccionada = Signal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.columnas: Dict[EstadoCotizacion, QVBoxLayout] = {}
        self._init_ui()

    def _init_ui(self):
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(12)

        # Estados principales a mostrar en Kanban
        estados_kanban = [
            EstadoCotizacion.BORRADOR,
            EstadoCotizacion.COTIZADA,
            EstadoCotizacion.ENVIADA_CLIENTE,
            EstadoCotizacion.ACEPTADA_CLIENTE,
            EstadoCotizacion.PENDIENTE_AREA_MEDICA,
            EstadoCotizacion.PROGRAMADA,
            EstadoCotizacion.OC_RECIBIDA,
            EstadoCotizacion.FACTURADA
        ]

        for estado in estados_kanban:
            col_widget = QWidget()
            col_layout = QVBoxLayout(col_widget)
            col_layout.setContentsMargins(8, 8, 8, 8)

            lbl_header = QLabel(f"<b>{estado.value}</b>")
            lbl_header.setStyleSheet("color: #374151; font-size: 13px; padding-bottom: 8px;")
            col_layout.addWidget(lbl_header)

            scroll = QScrollArea()
            scroll.setWidgetResizable(True)
            scroll_content = QWidget()
            cards_layout = QVBoxLayout(scroll_content)
            cards_layout.setContentsMargins(0, 0, 0, 0)
            cards_layout.addStretch()

            scroll.setWidget(scroll_content)
            col_layout.addWidget(scroll)

            self.columnas[estado] = cards_layout
            main_layout.addWidget(col_widget)

    def cargar_cotizaciones(self, cotizaciones: List[CotizacionDTO]):
        # Limpiar tarjetas existentes
        for layout in self.columnas.values():
            while layout.count() > 1:
                item = layout.takeAt(0)
                if item.widget():
                    item.widget().deleteLater()

        # Agregar nuevas tarjetas
        for dto in cotizaciones:
            if dto.estado in self.columnas:
                card = KanbanCard(dto)
                card.clicked.connect(self.cotizacion_seleccionada.emit)
                self.columnas[dto.estado].insertWidget(self.columnas[dto.estado].count() - 1, card)
