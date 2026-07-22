"""
Componente KPICard — Tarjeta de Metricas e Indicadores Clave.
"""

from PySide6.QtWidgets import QFrame, QVBoxLayout, QLabel


class KPICard(QFrame):
    """Tarjeta individual para despliegue de metricas numéricas o financieras."""

    def __init__(self, titulo: str, valor: str, subtexto: str = "", icono: str = "📊", parent=None):
        super().__init__(parent)
        self.setProperty("class", "kpi-card")
        self._init_ui(titulo, valor, subtexto, icono)

    def _init_ui(self, titulo: str, valor: str, subtexto: str, icono: str):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(4)

        lbl_titulo = QLabel(f"{icono} {titulo}")
        lbl_titulo.setProperty("class", "kpi-title")

        self.lbl_valor = QLabel(valor)
        self.lbl_valor.setProperty("class", "kpi-value")

        lbl_sub = QLabel(subtexto)
        lbl_sub.setStyleSheet("font-size: 11px; color: #6B7280;")

        layout.addWidget(lbl_titulo)
        layout.addWidget(self.lbl_valor)
        if subtexto:
            layout.addWidget(lbl_sub)

    def actualizar_valor(self, nuevo_valor: str):
        self.lbl_valor.setText(nuevo_valor)
