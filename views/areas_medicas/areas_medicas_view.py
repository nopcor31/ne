"""
Vista de Gestion de Areas Medicas y Revisiones Tecnicas Evaluadoras.
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTableWidgetItem,
    QDialog, QFormLayout, QLineEdit, QTextEdit, QCheckBox, QMessageBox
)
from controllers.area_medica_controller import AreaMedicaController
from views.components.modern_table import ModernTable


class RevisionMedicaDialog(QDialog):
    """Dialogo modal para responder una revision medica técnica."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Dictamen Técnico Médico")
        self.setMinimumWidth(400)
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(14)

        lbl_titulo = QLabel("<b>Dictamen de Evaluación Médica</b>")
        lbl_titulo.setStyleSheet("font-size: 16px; color: #0F172A;")
        layout.addWidget(lbl_titulo)

        form = QFormLayout()

        self.txt_envio_id = QLineEdit("1")
        self.chk_aprobado = QCheckBox("Aprobar Requerimiento Técnico y Equipos")
        self.chk_aprobado.setChecked(True)

        self.txt_observaciones = QTextEdit()
        self.txt_observaciones.setPlaceholderText("Comentarios sobre personal médico, ambulancias o equipos requeridos...")
        self.txt_observaciones.setMaximumHeight(90)

        form.addRow("ID Envío *:", self.txt_envio_id)
        form.addRow("Dictamen:", self.chk_aprobado)
        form.addRow("Observaciones Médicas:", self.txt_observaciones)

        layout.addLayout(form)

        btns = QHBoxLayout()
        btn_cancelar = QPushButton("Cancelar")
        btn_cancelar.setObjectName("btnSecondary")
        btn_cancelar.clicked.connect(self.reject)

        btn_guardar = QPushButton("Registrar Dictamen")
        btn_guardar.clicked.connect(self.accept)

        btns.addStretch()
        btns.addWidget(btn_cancelar)
        btns.addWidget(btn_guardar)
        layout.addLayout(btns)


class AreasMedicasView(QWidget):
    """Vista del modulo de revisiones tecnicas medicas."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.controller = AreaMedicaController()
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(16)

        header = QHBoxLayout()
        lbl_titulo = QLabel("<b>Áreas Médicas — Revisiones Técnicas</b>")
        lbl_titulo.setStyleSheet("font-size: 20px; color: #0F172A;")

        btn_revision = QPushButton("🏥 Registrar Dictamen Médico")
        btn_revision.clicked.connect(self._abrir_modal_dictamen)

        header.addWidget(lbl_titulo)
        header.addStretch()
        header.addWidget(btn_revision)

        layout.addLayout(header)

        self.tabla = ModernTable()
        self.tabla.setColumnCount(5)
        self.tabla.setHorizontalHeaderLabels(["ID Envío", "Cotización #", "Área Médica", "Estado Revisión", "Observaciones"])
        layout.addWidget(self.tabla)

        self.cargar_pendientes()

    def cargar_pendientes(self):
        try:
            pendientes = self.controller.obtener_envios_pendientes()
            self.tabla.setRowCount(len(pendientes))
            for row, env in enumerate(pendientes):
                self.tabla.setItem(row, 0, QTableWidgetItem(str(env.id)))
                self.tabla.setItem(row, 1, QTableWidgetItem(str(env.cotizacion_id)))
                self.tabla.setItem(row, 2, QTableWidgetItem(str(env.area_medica_id)))
                self.tabla.setItem(row, 3, QTableWidgetItem("Pendiente" if not env.respondido else ("Aprobado" if env.aprobado else "Rechazado")))
                self.tabla.setItem(row, 4, QTableWidgetItem(env.observaciones or "Sin observaciones"))
        except Exception as e:
            pass

    def _abrir_modal_dictamen(self):
        dialog = RevisionMedicaDialog(self)
        if dialog.exec() == QDialog.Accepted:
            try:
                envio_id = int(dialog.txt_envio_id.text().strip() or "1")
                aprobado = dialog.chk_aprobado.isChecked()
                obs = dialog.txt_observaciones.toPlainText().strip()

                self.controller.responder_revision(envio_id, aprobado, usuario_id=1, observaciones=obs)
                QMessageBox.information(self, "Dictamen Registrado", "La evaluación médica ha sido registrada correctamente.")
                self.cargar_pendientes()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"No se pudo registrar la revisión: {e}")
