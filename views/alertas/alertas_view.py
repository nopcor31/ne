"""
Vista del Centro de Alertas y Notificaciones Proactivas del Sistema.
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTableWidgetItem, QMessageBox
)
from controllers.alerta_controller import AlertaController
from views.components.modern_table import ModernTable


class AlertasView(QWidget):
    """Vista de monitoreo y atencion de alertas proactivas automatizadas."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.controller = AlertaController()
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(16)

        header = QHBoxLayout()
        lbl_titulo = QLabel("<b>Centro de Alertas Proactivas</b>")
        lbl_titulo.setStyleSheet("font-size: 20px; color: #0F172A;")

        btn_verificar = QPushButton("🔍 Verificar Alertas Proactivas")
        btn_verificar.clicked.connect(self._verificar_alertas_ahora)

        header.addWidget(lbl_titulo)
        header.addStretch()
        header.addWidget(btn_verificar)

        layout.addLayout(header)

        self.tabla = ModernTable()
        self.tabla.setColumnCount(6)
        self.tabla.setHorizontalHeaderLabels(["ID", "Tipo Alerta", "Título", "Mensaje / Detalle", "Prioridad", "Acciones"])
        layout.addWidget(self.tabla)

        self.cargar_alertas()

    def cargar_alertas(self):
        try:
            alertas = self.controller.obtener_alertas_no_resueltas()
            self.tabla.setRowCount(len(alertas))
            for row, a in enumerate(alertas):
                self.tabla.setItem(row, 0, QTableWidgetItem(str(a.id)))
                self.tabla.setItem(row, 1, QTableWidgetItem(str(a.tipo_alerta.value if hasattr(a.tipo_alerta, 'value') else a.tipo_alerta)))
                self.tabla.setItem(row, 2, QTableWidgetItem(a.titulo))
                self.tabla.setItem(row, 3, QTableWidgetItem(a.mensaje))
                self.tabla.setItem(row, 4, QTableWidgetItem(str(a.prioridad)))

                btn_resolver = QPushButton("✓ Atender")
                btn_resolver.setObjectName("btnSecondary")
                btn_resolver.clicked.connect(lambda _, a_id=a.id: self._resolver_alerta(a_id))
                self.tabla.setCellWidget(row, 5, btn_resolver)
        except Exception as e:
            pass

    def _verificar_alertas_ahora(self):
        try:
            generadas = self.controller.generar_alertas_proactivas()
            QMessageBox.information(self, "Verificación Completada", f"Se verificaron las condiciones del sistema. Nuevas alertas: {generadas}")
            self.cargar_alertas()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error verificando alertas: {e}")

    def _resolver_alerta(self, alerta_id: int):
        try:
            self.controller.marcar_como_resuelta(alerta_id, usuario_id=1)
            QMessageBox.information(self, "Alerta Atendida", f"Alerta #{alerta_id} marcada como resuelta.")
            self.cargar_alertas()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo resolver la alerta: {e}")
