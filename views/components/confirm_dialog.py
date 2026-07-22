"""
Componente ConfirmDialog — Modal de confirmacion reutilizable.
"""

from PySide6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton


class ConfirmDialog(QDialog):
    """Dialogo modal de confirmacion para acciones destructivas o importantes."""

    def __init__(self, titulo: str, mensaje: str, parent=None):
        super().__init__(parent)
        self.setWindowTitle(titulo)
        self.setMinimumWidth(360)
        self._init_ui(mensaje)

    def _init_ui(self, mensaje: str):
        layout = QVBoxLayout(self)
        layout.setSpacing(16)

        lbl_mensaje = QLabel(mensaje)
        lbl_mensaje.setWordWrap(True)
        layout.addWidget(lbl_mensaje)

        buttons_layout = QHBoxLayout()
        btn_cancelar = QPushButton("Cancelar")
        btn_cancelar.setObjectName("btnSecondary")
        btn_cancelar.clicked.connect(self.reject)

        btn_confirmar = QPushButton("Confirmar")
        btn_confirmar.clicked.connect(self.accept)

        buttons_layout.addStretch()
        buttons_layout.addWidget(btn_cancelar)
        buttons_layout.addWidget(btn_confirmar)

        layout.addLayout(buttons_layout)
