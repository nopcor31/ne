"""
Vista del Catalogo de Tarifas Generales y Especiales con filtros y modal de creacion.
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTableWidgetItem,
    QDialog, QFormLayout, QLineEdit, QComboBox, QDoubleSpinBox, QMessageBox
)
from controllers.tarifa_controller import TarifaController
from views.components.modern_table import ModernTable
from views.components.filter_bar import FilterBar


class NuevaTarifaDialog(QDialog):
    """Dialogo modal para definir una nueva tarifa comercial."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Configurar Nueva Tarifa")
        self.setMinimumWidth(400)
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(14)

        lbl_titulo = QLabel("<b>Parámetro de Tarifa Comercial</b>")
        lbl_titulo.setStyleSheet("font-size: 16px; color: #0F172A;")
        layout.addWidget(lbl_titulo)

        form = QFormLayout()

        self.txt_servicio_id = QLineEdit("1")
        self.txt_cliente_id = QLineEdit()
        self.txt_cliente_id.setPlaceholderText("Dejar en blanco para tarifa general")

        self.spn_valor_hora = QDoubleSpinBox()
        self.spn_valor_hora.setRange(0, 100000000)
        self.spn_valor_hora.setValue(150000)
        self.spn_valor_hora.setSingleStep(10000)
        self.spn_valor_hora.setPrefix("$ ")

        self.spn_valor_dia = QDoubleSpinBox()
        self.spn_valor_dia.setRange(0, 100000000)
        self.spn_valor_dia.setValue(1200000)
        self.spn_valor_dia.setSingleStep(50000)
        self.spn_valor_dia.setPrefix("$ ")

        form.addRow("ID Servicio *:", self.txt_servicio_id)
        form.addRow("ID Cliente (Opcional):", self.txt_cliente_id)
        form.addRow("Valor Hora (Diurna/Base) *:", self.spn_valor_hora)
        form.addRow("Valor Día (Base) *:", self.spn_valor_dia)

        layout.addLayout(form)

        btns = QHBoxLayout()
        btn_cancelar = QPushButton("Cancelar")
        btn_cancelar.setObjectName("btnSecondary")
        btn_cancelar.clicked.connect(self.reject)

        btn_guardar = QPushButton("Guardar Tarifa")
        btn_guardar.clicked.connect(self.accept)

        btns.addStretch()
        btns.addWidget(btn_cancelar)
        btns.addWidget(btn_guardar)
        layout.addLayout(btns)


class TarifasView(QWidget):
    """Vista de tarifas vigentes con listado interactivo."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.controller = TarifaController()
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(16)

        header = QHBoxLayout()
        lbl_titulo = QLabel("<b>Catálogo de Tarifas Comercial</b>")
        lbl_titulo.setStyleSheet("font-size: 20px; color: #0F172A;")
        btn_nueva = QPushButton("+ Nueva Tarifa")
        btn_nueva.clicked.connect(self._abrir_modal_nueva_tarifa)

        header.addWidget(lbl_titulo)
        header.addStretch()
        header.addWidget(btn_nueva)
        layout.addLayout(header)

        self.filter_bar = FilterBar()
        self.filter_bar.filtro_cambiado.connect(self.cargar_tarifas)
        layout.addWidget(self.filter_bar)

        self.tabla = ModernTable()
        self.tabla.setColumnCount(5)
        self.tabla.setHorizontalHeaderLabels(["ID Tarifa", "Servicio ID", "Cliente ID / Alcance", "Valor Hora", "Valor Día"])
        layout.addWidget(self.tabla)

        self.cargar_tarifas()

    def cargar_tarifas(self):
        try:
            tarifas = self.controller.obtener_tarifas_generales()
            self.tabla.setRowCount(len(tarifas))
            for row, t in enumerate(tarifas):
                alcance = f"Cliente #{t.cliente_id}" if getattr(t, 'cliente_id', None) else "General / Standard"
                self.tabla.setItem(row, 0, QTableWidgetItem(str(t.id)))
                self.tabla.setItem(row, 1, QTableWidgetItem(str(t.servicio_id)))
                self.tabla.setItem(row, 2, QTableWidgetItem(alcance))
                self.tabla.setItem(row, 3, QTableWidgetItem(f"${t.valor_hora:,.0f} COP"))
                self.tabla.setItem(row, 4, QTableWidgetItem(f"${t.valor_dia:,.0f} COP"))
        except Exception as e:
            pass

    def _abrir_modal_nueva_tarifa(self):
        dialog = NuevaTarifaDialog(self)
        if dialog.exec() == QDialog.Accepted:
            try:
                servicio_id = int(dialog.txt_servicio_id.text().strip() or "1")
                cliente_id = int(dialog.txt_cliente_id.text().strip()) if dialog.txt_cliente_id.text().strip() else None
                valor_hora = dialog.spn_valor_hora.value()
                valor_dia = dialog.spn_valor_dia.value()

                self.controller.crear_o_actualizar_tarifa(
                    cliente_id=cliente_id,
                    servicio_id=servicio_id,
                    valor_hora=valor_hora,
                    valor_dia=valor_dia,
                    usuario_id=1
                )
                QMessageBox.information(self, "Éxito", "Tarifa guardada correctamente.")
                self.cargar_tarifas()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"No se pudo guardar la tarifa: {e}")
