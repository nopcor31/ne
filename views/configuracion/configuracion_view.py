"""
Vista de Parametros y Configuracion General del Sistema CRM Operativo NE.
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFormLayout, QLineEdit, QPushButton,
    QSpinBox, QTextEdit, QMessageBox
)
from controllers.configuracion_controller import ConfiguracionController


class ConfiguracionView(QWidget):
    """Vista de parametros corporativos, integraciones y reglas de negocio."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.controller = ConfiguracionController()
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(16)

        header = QHBoxLayout()
        lbl_titulo = QLabel("<b>Configuración General y Parámetros</b>")
        lbl_titulo.setStyleSheet("font-size: 20px; color: #0F172A;")

        header.addWidget(lbl_titulo)
        header.addStretch()
        layout.addLayout(header)

        form = QFormLayout()
        form.setSpacing(14)

        self.txt_razon_social = QLineEdit("Servicios Médicos NE S.A.S.")
        self.txt_nit = QLineEdit("900.123.456-7")

        self.spn_dias_alerta = QSpinBox()
        self.spn_dias_alerta.setRange(1, 30)
        self.spn_dias_alerta.setValue(3)

        self.txt_asunto_email = QLineEdit("Cotización Servicios Médicos NE - {numero_cotizacion}")

        form.addRow("Razón Social Empresa:", self.txt_razon_social)
        form.addRow("NIT Empresarial:", self.txt_nit)
        form.addRow("Días Alerta Sin Respuesta Cliente:", self.spn_dias_alerta)
        form.addRow("Plantilla Asunto Email Outlook:", self.txt_asunto_email)

        layout.addLayout(form)

        btn_guardar = QPushButton("💾 Guardar Parámetros de Configuración")
        btn_guardar.clicked.connect(self._guardar_configuracion)
        layout.addWidget(btn_guardar)

        layout.addStretch()

        self.cargar_configuracion()

    def cargar_configuracion(self):
        try:
            config = self.controller.obtener_configuracion()
            if config:
                self.txt_razon_social.setText(config.get("razon_social", "Servicios Médicos NE S.A.S."))
                self.txt_nit.setText(config.get("nit", "900.123.456-7"))
                self.spn_dias_alerta.setValue(int(config.get("dias_alerta", 3)))
                self.txt_asunto_email.setText(config.get("asunto_email", "Cotización Servicios Médicos NE - {numero_cotizacion}"))
        except Exception as e:
            pass

    def _guardar_configuracion(self):
        try:
            datos = {
                "razon_social": self.txt_razon_social.text().strip(),
                "nit": self.txt_nit.text().strip(),
                "dias_alerta": self.spn_dias_alerta.value(),
                "asunto_email": self.txt_asunto_email.text().strip()
            }
            self.controller.guardar_configuracion(datos, usuario_id=1)
            QMessageBox.information(self, "Configuración Guardada", "Los parámetros del sistema han sido actualizados exitosamente.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo guardar la configuración: {e}")
