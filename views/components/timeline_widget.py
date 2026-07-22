"""
Componente TimelineWidget — Feed cronologico de actividad e interacciones.
"""

from typing import List
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame
from utils.formatters import formatear_fecha_hora


class TimelineWidget(QWidget):
    """Widget de linea de tiempo para despliegue de trazabilidad e historial."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout_main = QVBoxLayout(self)
        self.layout_main.setContentsMargins(0, 0, 0, 0)
        self.layout_main.setSpacing(8)

    def cargar_eventos(self, eventos: List[Any]):
        # Limpiar
        while self.layout_main.count():
            item = self.layout_main.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        for ev in eventos:
            card = QFrame()
            card.setStyleSheet("background-color: #FFFFFF; border-left: 3px solid #1B6FD8; padding: 8px;")
            l = QVBoxLayout(card)
            fecha_str = formatear_fecha_hora(getattr(ev, "fecha_hora", None))
            accion_str = getattr(ev, "accion", getattr(ev, "asunto", "Evento"))
            detalle_str = getattr(ev, "detalle", getattr(ev, "descripcion", ""))

            lbl_header = QLabel(f"<b>{accion_str}</b> — <small>{fecha_str}</small>")
            lbl_det = QLabel(detalle_str or "Sin detalles adicionales")
            lbl_det.setStyleSheet("color: #6B7280; font-size: 12px;")

            l.addWidget(lbl_header)
            l.addWidget(lbl_det)
            self.layout_main.addWidget(card)

        self.layout_main.addStretch()
