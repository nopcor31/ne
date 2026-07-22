"""
Vista Principal del Pipeline de Cotizaciones (Lista / Kanban, Modales, PDF y Acciones).
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QStackedWidget,
    QTableWidgetItem, QDialog, QFormLayout, QLineEdit, QTextEdit, QMessageBox,
    QComboBox, QSplitter
)
from PySide6.QtCore import Qt
from controllers.cotizacion_controller import CotizacionController
from services.dto.cotizacion_dto import CotizacionDTO
from views.components.modern_table import ModernTable
from views.components.kanban_board import KanbanBoard
from views.components.filter_bar import FilterBar
from views.components.progress_steps import ProgressSteps
from views.components.state_badge import StateBadge
from core.enums import EstadoCotizacion


class NuevaCotizacionDialog(QDialog):
    """Dialogo modal para la creacion de un borrador de cotizacion."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Crear Nueva Cotización (Borrador)")
        self.setMinimumWidth(440)
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(14)

        lbl_titulo = QLabel("<b>Nueva Cotización Comercial</b>")
        lbl_titulo.setStyleSheet("font-size: 16px; color: #0F172A;")
        layout.addWidget(lbl_titulo)

        form = QFormLayout()

        self.txt_cliente_id = QLineEdit("1")
        self.txt_cliente_id.setPlaceholderText("ID Numérico del Cliente")

        self.txt_contacto_id = QLineEdit()
        self.txt_contacto_id.setPlaceholderText("ID del Contacto (Opcional)")

        self.txt_observaciones = QTextEdit()
        self.txt_observaciones.setPlaceholderText("Observaciones o requerimientos de la propuesta médica...")
        self.txt_observaciones.setMaximumHeight(90)

        form.addRow("ID Cliente *:", self.txt_cliente_id)
        form.addRow("ID Contacto:", self.txt_contacto_id)
        form.addRow("Observaciones:", self.txt_observaciones)

        layout.addLayout(form)

        btns = QHBoxLayout()
        btn_cancelar = QPushButton("Cancelar")
        btn_cancelar.setObjectName("btnSecondary")
        btn_cancelar.clicked.connect(self.reject)

        btn_guardar = QPushButton("Crear Borrador")
        btn_guardar.clicked.connect(self.accept)

        btns.addStretch()
        btns.addWidget(btn_cancelar)
        btns.addWidget(btn_guardar)
        layout.addLayout(btns)


class CotizacionesView(QWidget):
    """Vista principal con selector de vista (Lista / Kanban), acciones de PDF/Email y filtrado."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.controller = CotizacionController()
        self.cotizaciones_list: list[CotizacionDTO] = []
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(16)

        header = QHBoxLayout()
        lbl_titulo = QLabel("<b>Pipeline de Cotizaciones</b>")
        lbl_titulo.setStyleSheet("font-size: 20px; color: #0F172A;")

        self.btn_toggle_vista = QPushButton("🗂 Modo Kanban / Lista")
        self.btn_toggle_vista.setObjectName("btnSecondary")
        self.btn_toggle_vista.clicked.connect(self._toggle_vista)

        btn_nueva = QPushButton("+ Nueva Cotización")
        btn_nueva.clicked.connect(self._abrir_modal_nueva)

        header.addWidget(lbl_titulo)
        header.addStretch()
        header.addWidget(self.btn_toggle_vista)
        header.addWidget(btn_nueva)

        layout.addLayout(header)

        # Barra de Filtros
        self.filter_bar = FilterBar()
        self.filter_bar.txt_buscar.setPlaceholderText("Buscar por # Cotización, Cliente...")
        self.filter_bar.combo_estado.clear()
        self.filter_bar.combo_estado.addItem("Todos los Estados")
        for st in EstadoCotizacion:
            self.filter_bar.combo_estado.addItem(st.value, st)
        self.filter_bar.filtro_cambiado.connect(self._aplicar_filtros)
        layout.addWidget(self.filter_bar)

        self.stack_vistas = QStackedWidget()

        # Vista 0: Tabla Lista
        self.tabla = ModernTable()
        self.tabla.setColumnCount(6)
        self.tabla.setHorizontalHeaderLabels(["Número", "Cliente", "Estado", "Valor Total", "Fecha", "Acciones"])
        self.tabla.doubleClicked.connect(self._on_doble_click_fila)
        self.stack_vistas.addWidget(self.tabla)

        # Vista 1: Kanban Board
        self.kanban = KanbanBoard()
        self.kanban.cotizacion_seleccionada.connect(self._on_cotizacion_kanban_click)
        self.stack_vistas.addWidget(self.kanban)

        layout.addWidget(self.stack_vistas)

        self.cargar_cotizaciones()

    def cargar_cotizaciones(self):
        try:
            self.cotizaciones_list = self.controller.listar_cotizaciones()
            self._mostrar_en_tabla_y_kanban(self.cotizaciones_list)
        except Exception as e:
            pass

    def _mostrar_en_tabla_y_kanban(self, lista: list[CotizacionDTO]):
        # Cargar Tabla
        self.tabla.setRowCount(len(lista))
        for row, cot in enumerate(lista):
            self.tabla.setItem(row, 0, QTableWidgetItem(cot.numero_cotizacion))
            self.tabla.setItem(row, 1, QTableWidgetItem(cot.cliente_nombre or f"Cliente #{cot.cliente_id}"))

            # State badge item
            badge = StateBadge(cot.estado)
            self.tabla.setCellWidget(row, 2, badge)

            self.tabla.setItem(row, 3, QTableWidgetItem(f"${cot.valor_total:,.0f} COP"))
            fecha_str = cot.fecha_creacion.strftime("%Y-%m-%d %H:%M") if cot.fecha_creacion else "N/A"
            self.tabla.setItem(row, 4, QTableWidgetItem(fecha_str))

            # Boton Accion PDF / Email
            btn_pdf = QPushButton("📄 PDF / Email")
            btn_pdf.setObjectName("btnSecondary")
            btn_pdf.clicked.connect(lambda _, c_id=cot.id: self._generar_pdf_email(c_id))
            self.tabla.setCellWidget(row, 5, btn_pdf)

        # Cargar Kanban
        self.kanban.cargar_cotizaciones(lista)

    def _aplicar_filtros(self):
        texto = self.filter_bar.txt_buscar.text().strip().lower()
        estado_sel = self.filter_bar.combo_estado.currentData()

        filtrados = self.cotizaciones_list
        if estado_sel and isinstance(estado_sel, EstadoCotizacion):
            filtrados = [c for c in filtrados if c.estado == estado_sel]

        if texto:
            filtrados = [
                c for c in filtrados
                if texto in c.numero_cotizacion.lower() or (c.cliente_nombre and texto in c.cliente_nombre.lower())
            ]

        self._mostrar_en_tabla_y_kanban(filtrados)

    def _toggle_vista(self):
        current = self.stack_vistas.currentIndex()
        self.stack_vistas.setCurrentIndex(1 if current == 0 else 0)

    def _abrir_modal_nueva(self):
        dialog = NuevaCotizacionDialog(self)
        if dialog.exec() == QDialog.Accepted:
            try:
                cliente_id = int(dialog.txt_cliente_id.text().strip() or "1")
                contacto_id = int(dialog.txt_contacto_id.text().strip()) if dialog.txt_contacto_id.text().strip() else None
                obs = dialog.txt_observaciones.toPlainText().strip()

                cot_id = self.controller.crear_borrador(
                    cliente_id=cliente_id,
                    usuario_creador_id=1,
                    contacto_id=contacto_id,
                    observaciones=obs
                )
                QMessageBox.information(self, "Cotización Creada", f"Borrador creado exitosamente con ID #{cot_id}.")
                self.cargar_cotizaciones()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"No se pudo crear la cotización: {e}")

    def _generar_pdf_email(self, cotizacion_id: int):
        try:
            pdf_path = self.controller.generar_pdf_y_enviar_email(cotizacion_id, usuario_id=1)
            QMessageBox.information(self, "PDF Generado", f"El archivo PDF formal fue generado en:\n{pdf_path}")
            self.cargar_cotizaciones()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error generando PDF/Email: {e}")

    def _on_doble_click_fila(self, index):
        row = index.row()
        if 0 <= row < len(self.cotizaciones_list):
            cot = self.cotizaciones_list[row]
            self._mostrar_detalle_cotizacion(cot)

    def _on_cotizacion_kanban_click(self, cotizacion_id: int):
        cot = self.controller.obtener_por_id(cotizacion_id)
        if cot:
            self._mostrar_detalle_cotizacion(cot)

    def _mostrar_detalle_cotizacion(self, cot: CotizacionDTO):
        msg = f"Cotización: {cot.numero_cotizacion}\nEstado: {cot.estado.value}\nValor Total: ${cot.valor_total:,.0f} COP"
        QMessageBox.information(self, f"Expediente #{cot.numero_cotizacion}", msg)
