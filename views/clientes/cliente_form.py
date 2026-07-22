"""
Formulario Modal / Dialogo para Creacion y Edicion de Cliente.
"""

from PySide6.QtWidgets import QDialog, QVBoxLayout, QFormLayout, QLineEdit, QComboBox, QPushButton, QHBoxLayout
from core.enums import TipoCliente


class ClienteForm(QDialog):
    """Formulario para captura de campos basicos de un cliente."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Crear / Editar Cliente")
        self.setMinimumWidth(400)
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        form = QFormLayout()

        self.txt_empresa = QLineEdit()
        self.txt_nit = QLineEdit()
        self.txt_correo = QLineEdit()
        self.txt_telefono = QLineEdit()

        self.combo_tipo = QComboBox()
        self.combo_tipo.addItems([t.value for t in TipoCliente])

        form.addRow("Empresa:", self.txt_empresa)
        form.addRow("NIT:", self.txt_nit)
        form.addRow("Correo Principal:", self.txt_correo)
        form.addRow("Teléfono:", self.txt_telefono)
        form.addRow("Tipo Cliente:", self.combo_tipo)

        layout.addLayout(form)

        btns = QHBoxLayout()
        btn_cancelar = QPushButton("Cancelar")
        btn_cancelar.clicked.connect(self.reject)
        btn_guardar = QPushButton("Guardar Cliente")
        btn_guardar.clicked.connect(self.accept)

        btns.addStretch()
        btns.addWidget(btn_cancelar)
        btns.addWidget(btn_guardar)

        layout.addLayout(btns)
