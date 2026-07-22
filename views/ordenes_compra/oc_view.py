"""
Vista de Control y Seguimiento de Ordenes de Compra (OC).
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTableWidgetItem,
    QDialog, QFormLayout, QLineEdit, QTextEdit, QMessageBox
)
from controllers.oc_controller import OCController
from views.components.modern_table import ModernTable


class RegistrarOCDialog(QDialog):
    """Dialogo modal para registrar una Orden de Compra recibida del cliente."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Registrar Orden de Compra (OC)")
        self.setMinimumWidth(400)
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(14)

        lbl_titulo = QLabel("<b>Recepción de Orden de Compra Cliente</b>")
        lbl_titulo.setStyleSheet("font-size: 16px; color: #0F172A;")
        layout.addWidget(lbl_titulo)

        form = QFormLayout()

        self.txt_cotizacion_id = QLineEdit("1")
        self.txt_numero_oc = QLineEdit()
        self.txt_numero_oc.setPlaceholderText("Ej: OC-2026-9948")

        self.txt_archivo_path = QLineEdit()
        self.txt_archivo_path.setPlaceholderText("Ruta del archivo digital o escaneo PDF")

        self.txt_observaciones = QTextEdit()
        self.txt_observaciones.setMaximumHeight(80)

        form.addRow("ID Cotización *:", self.txt_cotizacion_id)
        form.addRow("Número de OC *:", self.txt_numero_oc)
        form.addRow("Ruta Archivo Adjunto:", self.txt_archivo_path)
        form.addRow("Observaciones:", self.txt_observaciones)

        layout.addLayout(form)

        btns = QHBoxLayout()
        btn_cancelar = QPushButton("Cancelar")
        btn_cancelar.setObjectName("btnSecondary")
        btn_cancelar.clicked.connect(self.reject)

        btn_guardar = QPushButton("Registrar OC")
        btn_guardar.clicked.connect(self.accept)

        btns.addStretch()
        btns.addWidget(btn_cancelar)
        btns.addWidget(btn_guardar)
        layout.addLayout(btns)


class OCView(QWidget):
    """Vista para el seguimiento de solicitudes y recepcion de Ordenes de Compra."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.controller = OCController()
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(16)

        header = QHBoxLayout()
        lbl_titulo = QLabel("<b>Control de Órdenes de Compra (OC)</b>")
        lbl_titulo.setStyleSheet("font-size: 20px; color: #0F172A;")

        btn_solicitar = QPushButton("✉ Solicitar OC al Cliente")
        btn_solicitar.setObjectName("btnSecondary")
        btn_solicitar.clicked.connect(self._solicitar_oc_cliente)

        btn_recibir = QPushButton("📦 Registrar OC Recibida")
        btn_recibir.clicked.connect(self._abrir_modal_recibir_oc)

        header.addWidget(lbl_titulo)
        header.addStretch()
        header.addWidget(btn_solicitar)
        header.addWidget(btn_recibir)

        layout.addLayout(header)

        self.tabla = ModernTable()
        self.tabla.setColumnCount(5)
        self.tabla.setHorizontalHeaderLabels(["Cotización #", "Cliente ID", "Fecha Solicitud", "Número OC Recibida", "Estado OC"])
        layout.addWidget(self.tabla)

        self.cargar_pendientes_oc()

    def cargar_pendientes_oc(self):
        try:
            pendientes = self.controller.obtener_ordenes_compra_pendientes()
            self.tabla.setRowCount(len(pendientes))
            for row, item in enumerate(pendientes):
                self.tabla.setItem(row, 0, QTableWidgetItem(str(item.numero_cotizacion if hasattr(item, 'numero_cotizacion') else item.id)))
                self.tabla.setItem(row, 1, QTableWidgetItem(str(item.cliente_id)))
                self.tabla.setItem(row, 2, QTableWidgetItem(str(getattr(item, 'fecha_creacion', 'N/A'))))
                self.tabla.setItem(row, 3, QTableWidgetItem(str(getattr(item, 'numero_oc', 'Pendiente'))))
                self.tabla.setItem(row, 4, QTableWidgetItem(str(getattr(item, 'estado', 'OC Pendiente'))))
        except Exception as e:
            pass

    def _solicitar_oc_cliente(self):
        try:
            self.controller.solicitar_oc(cotizacion_id=1, usuario_id=1)
            QMessageBox.information(self, "Solicitud Enviada", "Se ha notificado al cliente la solicitud de la Orden de Compra.")
            self.cargar_pendientes_oc()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo solicitar la OC: {e}")

    def _abrir_modal_recibir_oc(self):
        dialog = RegistrarOCDialog(self)
        if dialog.exec() == QDialog.Accepted:
            try:
                cot_id = int(dialog.txt_cotizacion_id.text().strip() or "1")
                num_oc = dialog.txt_numero_oc.text().strip()
                f_path = dialog.txt_archivo_path.text().strip()
                obs = dialog.txt_observaciones.toPlainText().strip()

                if not num_oc:
                    QMessageBox.warning(self, "Campo Requerido", "Debe ingresar el número de Orden de Compra.")
                    return

                self.controller.registrar_recibido_oc(cot_id, num_oc, usuario_id=1, archivo_path=f_path, observaciones=obs)
                QMessageBox.information(self, "Éxito", f"Orden de Compra #{num_oc} registrada exitosamente.")
                self.cargar_pendientes_oc()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"No se pudo registrar la OC: {e}")
