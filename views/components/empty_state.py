"""
Componente EmptyState — Ilustracion y mensaje cuando no hay datos.
"""

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Signal, Qt


class EmptyState(QWidget):
    """Estado vacio elegante con mensaje y boton de llamada a la accion (CTA)."""

    accion_solicitada = Signal()

    def __init__(self, titulo: str, mensaje: str, texto_boton: str = "", icono: str = "📭", parent=None):
        super().__init__(parent)
        self._init_ui(titulo, mensaje, texto_boton, icono)

    def _init_ui(self, titulo: str, mensaje: str, texto_boton: str, icono: str):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(12)

        lbl_icono = QLabel(icono)
        lbl_icono.setStyleSheet("font-size: 48px;")
        lbl_icono.setAlignment(Qt.AlignCenter)

        lbl_titulo = QLabel(f"<b>{titulo}</b>")
        lbl_titulo.setStyleSheet("font-size: 16px; color: #111827;")
        lbl_titulo.setAlignment(Qt.AlignCenter)

        lbl_msg = QLabel(mensaje)
        lbl_msg.setStyleSheet("color: #6B7280; font-size: 13px;")
        lbl_msg.setAlignment(Qt.AlignCenter)

        layout.addWidget(lbl_icono)
        layout.addWidget(lbl_titulo)
        layout.addWidget(lbl_msg)

        if texto_boton:
            btn_cta = QPushButton(texto_boton)
            btn_cta.clicked.connect(self.accion_solicitada.emit)
            layout.addWidget(btn_cta, alignment=Qt.AlignCenter)
