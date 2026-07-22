"""
Componente KanbanCard — Tarjeta individual para vista Kanban de cotizaciones.
"""

from PySide6.QtWidgets import QFrame, QVBoxLayout, QLabel
from PySide6.QtCore import Signal
from services.dto.cotizacion_dto import CotizacionDTO


class KanbanCard(QFrame):
    """Tarjeta Kanban que representa un expediente de cotizacion."""

    clicked = Signal(int)

    def __init__(self, cotizacion_dto: CotizacionDTO, parent=None):
        super().__init__(parent)
        self.cotizacion_id = cotizacion_dto.id
        self.setStyleSheet(
            "KanbanCard { background-color: #FFFFFF; border: 1px solid #E2E6EC; "
            "border-radius: 8px; padding: 8px; }"
            "KanbanCard:hover { border: 1px solid #1B6FD8; background-color: #F8FAFC; }"
        )
        self._init_ui(cotizacion_dto)

    def _init_ui(self, dto: CotizacionDTO):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(4)

        lbl_numero = QLabel(f"<b>{dto.numero_cotizacion}</b>")
        lbl_cliente = QLabel(dto.cliente_nombre or f"Cliente ID #{dto.cliente_id}")
        lbl_cliente.setStyleSheet("color: #6B7280; font-size: 12px;")

        lbl_total = QLabel(f"<b>${dto.valor_total:,.0f} COP</b>")
        lbl_total.setStyleSheet("color: #1B6FD8; font-size: 13px;")

        layout.addWidget(lbl_numero)
        layout.addWidget(lbl_cliente)
        layout.addWidget(lbl_total)

    def mousePressEvent(self, event):
        if self.cotizacion_id:
            self.clicked.emit(self.cotizacion_id)
        super().mousePressEvent(event)
