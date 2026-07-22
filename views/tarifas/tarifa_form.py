"""
Formulario Modal para Edición de Tarifa.
"""

from PySide6.QtWidgets import QDialog, QVBoxLayout, QFormLayout, QLineEdit, QComboBox, QPushButton


class TarifaForm(QDialog):
    """Formulario para creacion y modificacion de tarifas."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Registrar Tarifa")
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        form = QFormLayout()

        self.combo_ciudad = QComboBox()
        self.combo_servicio = QComboBox()
        self.txt_valor = QLineEdit()

        form.addRow("Ciudad:", self.combo_ciudad)
        form.addRow("Servicio:", self.combo_servicio)
        form.addRow("Valor Hora (COP):", self.txt_valor)

        layout.addLayout(form)

        btn_guardar = QPushButton("Guardar")
        btn_guardar.clicked.connect(self.accept)
        layout.addWidget(btn_guardar)
