"""
Vista de Control de Facturacion y Registro de Pagos.
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTableWidgetItem,
    QDialog, QFormLayout, QLineEdit, QDoubleSpinBox, QMessageBox
)
from controllers.facturacion_controller import FacturacionController
from views.components.modern_table import ModernTable


class RegistrarPagoDialog(QDialog):
    """Dialogo modal para registrar pago recibido de una factura."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Registrar Pago de Factura")
        self.setMinimumWidth(380)
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(14)

        lbl_titulo = QLabel("<b>Abono / Pago de Factura</b>")
        lbl_titulo.setStyleSheet("font-size: 16px; color: #0F172A;")
        layout.addWidget(lbl_titulo)

        form = QFormLayout()

        self.txt_factura_id = QLineEdit("1")

        self.spn_monto = QDoubleSpinBox()
        self.spn_monto.setRange(0, 1000000000)
        self.spn_monto.setValue(5000000)
        self.spn_monto.setSingleStep(100000)
        self.spn_monto.setPrefix("$ ")

        self.txt_metodo = QLineEdit("Transferencia Bancaria")

        form.addRow("ID Factura *:", self.txt_factura_id)
        form.addRow("Monto Recibido *:", self.spn_monto)
        form.addRow("Método de Pago:", self.txt_metodo)

        layout.addLayout(form)

        btns = QHBoxLayout()
        btn_cancelar = QPushButton("Cancelar")
        btn_cancelar.setObjectName("btnSecondary")
        btn_cancelar.clicked.connect(self.reject)

        btn_guardar = QPushButton("Registrar Pago")
        btn_guardar.clicked.connect(self.accept)

        btns.addStretch()
        btns.addWidget(btn_cancelar)
        btns.addWidget(btn_guardar)
        layout.addLayout(btns)


class FacturacionView(QWidget):
    """Vista para la emision de facturas y seguimiento de cobros."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.controller = FacturacionController()
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(16)

        header = QHBoxLayout()
        lbl_titulo = QLabel("<b>Módulo de Facturación y Cobros</b>")
        lbl_titulo.setStyleSheet("font-size: 20px; color: #0F172A;")

        btn_generar = QPushButton("🧾 Generar Factura de Cotización")
        btn_generar.clicked.connect(self._generar_factura)

        btn_pago = QPushButton("💰 Registrar Pago Recibido")
        btn_pago.setObjectName("btnSecondary")
        btn_pago.clicked.connect(self._abrir_modal_pago)

        header.addWidget(lbl_titulo)
        header.addStretch()
        header.addWidget(btn_generar)
        header.addWidget(btn_pago)

        layout.addLayout(header)

        self.tabla = ModernTable()
        self.tabla.setColumnCount(6)
        self.tabla.setHorizontalHeaderLabels(["ID Factura", "Cotización #", "Fecha Emisión", "Vencimiento", "Valor Facturado", "Estado"])
        layout.addWidget(self.tabla)

        self.cargar_facturas()

    def cargar_facturas(self):
        try:
            facturas = self.controller.obtener_facturas_pendientes()
            self.tabla.setRowCount(len(facturas))
            for row, f in enumerate(facturas):
                self.tabla.setItem(row, 0, QTableWidgetItem(str(f.id)))
                self.tabla.setItem(row, 1, QTableWidgetItem(str(f.cotizacion_id)))
                self.tabla.setItem(row, 2, QTableWidgetItem(str(getattr(f, 'fecha_emision', 'N/A'))))
                self.tabla.setItem(row, 3, QTableWidgetItem(str(getattr(f, 'fecha_vencimiento', 'N/A'))))
                self.tabla.setItem(row, 4, QTableWidgetItem(f"${getattr(f, 'valor_total', 0):,.0f} COP"))
                self.tabla.setItem(row, 5, QTableWidgetItem(str(getattr(f, 'estado', 'Emitida'))))
        except Exception as e:
            pass

    def _generar_factura(self):
        try:
            fac_id = self.controller.generar_factura(cotizacion_id=1, usuario_id=1)
            QMessageBox.information(self, "Factura Emitida", f"Se ha emitido la factura ID #{fac_id} correctamente.")
            self.cargar_facturas()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo generar la factura: {e}")

    def _abrir_modal_pago(self):
        dialog = RegistrarPagoDialog(self)
        if dialog.exec() == QDialog.Accepted:
            try:
                fac_id = int(dialog.txt_factura_id.text().strip() or "1")
                monto = dialog.spn_monto.value()
                metodo = dialog.txt_metodo.text().strip()

                self.controller.registrar_pago(fac_id, monto, usuario_id=1, metodo_pago=metodo)
                QMessageBox.information(self, "Pago Registrado", f"Pago de ${monto:,.0f} registrado con éxito.")
                self.cargar_facturas()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"No se pudo registrar el pago: {e}")
