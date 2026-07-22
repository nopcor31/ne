"""
Componente AlertBell — Icono de notificacion con contador de alertas.
"""

from PySide6.QtWidgets import QPushButton


class AlertBell(QPushButton):
    """Boton con icono de campanita y badge con conteo de alertas activas."""

    def __init__(self, parent=None):
        super().__init__("🔔 0", parent)
        self.setStyleSheet(
            "QPushButton { background-color: #F4F6FA; border: 1px solid #E2E6EC; "
            "border-radius: 14px; padding: 4px 12px; font-weight: bold; color: #1B6FD8; }"
            "QPushButton:hover { background-color: #E8F0FD; }"
        )

    def actualizar_conteo(self, cantidad: int):
        """Actualiza la cifra visual del contador de alertas."""
        self.setText(f"🔔 {cantidad}")
        if cantidad > 0:
            self.setStyleSheet(
                "QPushButton { background-color: #FEF2F2; border: 1px solid #FCA5A5; "
                "border-radius: 14px; padding: 4px 12px; font-weight: bold; color: #EF4444; }"
                "QPushButton:hover { background-color: #FEE2E2; }"
            )
        else:
            self.setStyleSheet(
                "QPushButton { background-color: #F4F6FA; border: 1px solid #E2E6EC; "
                "border-radius: 14px; padding: 4px 12px; font-weight: bold; color: #1B6FD8; }"
            )
