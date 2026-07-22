"""
Formulario Modal para Agregar / Editar Evento de Servicio.
"""

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QComboBox, QDateEdit, QTimeEdit,
    QLineEdit, QTextEdit, QPushButton, QHBoxLayout
)
from PySide6.QtCore import QDate, QTime


class EventoForm(QDialog):
    """Formulario para captura de datos de un evento de servicio."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Agregar Evento de Servicio")
        self.setMinimumWidth(500)
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        form = QFormLayout()

        self.combo_servicio = QComboBox()
        self.combo_ciudad = QComboBox()
        self.dt_fecha = QDateEdit(QDate.currentDate())
        self.tm_inicio = QTimeEdit(QTime(14, 0))
        self.tm_fin = QTimeEdit(QTime(20, 0))
        self.txt_direccion = QLineEdit()
        self.txt_contacto = QLineEdit()
        self.txt_telefono = QLineEdit()
        self.txt_obs = QTextEdit()

        form.addRow("Servicio:", self.combo_servicio)
        form.addRow("Ciudad:", self.combo_ciudad)
        form.addRow("Fecha:", self.dt_fecha)
        form.addRow("Hora Inicio:", self.tm_inicio)
        form.addRow("Hora Fin:", self.tm_fin)
        form.addRow("Dirección:", self.txt_direccion)
        form.addRow("Contacto:", self.txt_contacto)
        form.addRow("Teléfono:", self.txt_telefono)
        form.addRow("Observaciones:", self.txt_obs)

        layout.addLayout(form)

        btns = QHBoxLayout()
        btn_cancelar = QPushButton("Cancelar")
        btn_cancelar.clicked.connect(self.reject)
        btn_guardar = QPushButton("Calcular y Guardar Evento")
        btn_guardar.clicked.connect(self.accept)

        btns.addStretch()
        btns.addWidget(btn_cancelar)
        btns.addWidget(btn_guardar)

        layout.addLayout(btns)
