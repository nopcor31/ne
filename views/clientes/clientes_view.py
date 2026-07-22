"""
Vista del Catalogo y Gestion CRM de Clientes con busqueda, filtros, drawer lateral y dialogos.
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTableWidgetItem,
    QDialog, QFormLayout, QLineEdit, QComboBox, QTextEdit, QMessageBox, QSplitter
)
from PySide6.QtCore import Qt
from controllers.cliente_controller import ClienteController
from services.dto.cliente_dto import ClienteDTO, ContactoDTO
from views.components.modern_table import ModernTable
from views.components.filter_bar import FilterBar
from views.components.drawer_panel import DrawerPanel
from core.enums import TipoCliente, SectorCliente


class NuevoClienteDialog(QDialog):
    """Dialogo modal para registro de un nuevo cliente."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Registrar Nuevo Cliente")
        self.setMinimumWidth(480)
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(14)

        lbl_titulo = QLabel("<b>Nuevo Cliente Empresarial</b>")
        lbl_titulo.setStyleSheet("font-size: 16px; color: #0F172A;")
        layout.addWidget(lbl_titulo)

        form = QFormLayout()
        self.txt_empresa = QLineEdit()
        self.txt_empresa.setPlaceholderText("Nombre de la Empresa o Razon Social")

        self.txt_nit = QLineEdit()
        self.txt_nit.setPlaceholderText("Ej: 900.123.456-7")

        self.combo_tipo = QComboBox()
        for t in TipoCliente:
            self.combo_tipo.addItem(t.value, t)

        self.combo_sector = QComboBox()
        for s in SectorCliente:
            self.combo_sector.addItem(s.value, s)

        self.txt_correo = QLineEdit()
        self.txt_correo.setPlaceholderText("correo@empresa.com")

        self.txt_telefono = QLineEdit()
        self.txt_telefono.setPlaceholderText("+57 300 123 4567")

        self.txt_direccion = QLineEdit()
        self.txt_direccion.setPlaceholderText("Calle/Carrera # No.")

        self.txt_observaciones = QTextEdit()
        self.txt_observaciones.setMaximumHeight(80)

        form.addRow("Empresa *:", self.txt_empresa)
        form.addRow("NIT *:", self.txt_nit)
        form.addRow("Tipo Cliente:", self.combo_tipo)
        form.addRow("Sector:", self.combo_sector)
        form.addRow("Correo Principal *:", self.txt_correo)
        form.addRow("Teléfono:", self.txt_telefono)
        form.addRow("Dirección:", self.txt_direccion)
        form.addRow("Observaciones:", self.txt_observaciones)

        layout.addLayout(form)

        btns = QHBoxLayout()
        btn_cancelar = QPushButton("Cancelar")
        btn_cancelar.setObjectName("btnSecondary")
        btn_cancelar.clicked.connect(self.reject)

        btn_guardar = QPushButton("Guardar Cliente")
        btn_guardar.clicked.connect(self.accept)

        btns.addStretch()
        btns.addWidget(btn_cancelar)
        btns.addWidget(btn_guardar)
        layout.addLayout(btns)

    def get_dto((self)) -> ClienteDTO:
        return ClienteDTO(
            empresa=self.txt_empresa.text().strip(),
            nit=self.txt_nit.text().strip(),
            tipo_cliente=self.combo_tipo.currentData(),
            sector=self.combo_sector.currentData(),
            correo_principal=self.txt_correo.text().strip(),
            telefono_principal=self.txt_telefono.text().strip(),
            direccion=self.txt_direccion.text().strip(),
            observaciones=self.txt_observaciones.toPlainText().strip()
        )


class ClientesView(QWidget):
    """Vista de gestion de clientes con filtros, splitter y panel lateral de detalle."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.controller = ClienteController()
        self.clientes_list: list[ClienteDTO] = []
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(16)

        # Header
        header = QHBoxLayout()
        lbl_titulo = QLabel("<b>Gestión de Clientes (CRM)</b>")
        lbl_titulo.setStyleSheet("font-size: 20px; color: #0F172A;")

        btn_nuevo = QPushButton("+ Nuevo Cliente")
        btn_nuevo.clicked.connect(self._abrir_modal_nuevo_cliente)

        header.addWidget(lbl_titulo)
        header.addStretch()
        header.addWidget(btn_nuevo)
        layout.addLayout(header)

        # Barra de Filtros
        self.filter_bar = FilterBar()
        self.filter_bar.txt_buscar.setPlaceholderText("Buscar por Empresa, NIT, Correo...")
        self.filter_bar.filtro_cambiado.connect(self._filtrar_clientes)
        layout.addWidget(self.filter_bar)

        # Splitter principal para Tabla + Drawer
        self.splitter = QSplitter(Qt.Horizontal)

        # Tabla de Clientes
        self.tabla = ModernTable()
        self.tabla.setColumnCount(5)
        self.tabla.setHorizontalHeaderLabels(["Empresa", "NIT", "Tipo Cliente", "Correo Principal", "Teléfono"])
        self.tabla.itemSelectionChanged.connect(self._on_cliente_seleccionado)
        self.splitter.addWidget(self.tabla)

        # Drawer Lateral de Detalle
        self.drawer = DrawerPanel("Detalles del Cliente")
        self.drawer.hide()
        self.drawer.cerrado.connect(self._cerrar_drawer)

        self.lbl_detalle_info = QLabel("Seleccione un cliente para ver detalles")
        self.lbl_detalle_info.setWordWrap(True)
        self.lbl_detalle_info.setStyleSheet("color: #475569; font-size: 13px; padding-top: 10px;")
        self.drawer.set_content(self.lbl_detalle_info)

        self.splitter.addWidget(self.drawer)
        self.splitter.setSizes([750, 350])

        layout.addWidget(self.splitter)

        self.cargar_clientes()

    def cargar_clientes(self):
        try:
            self.clientes_list = self.controller.listar_clientes()
            self._mostrar_clientes_en_tabla(self.clientes_list)
        except Exception as e:
            QMessageBox.warning(self, "Error", f"No se pudieron cargar los clientes: {e}")

    def _mostrar_clientes_en_tabla(self, lista: list[ClienteDTO]):
        self.tabla.setRowCount(len(lista))
        for row, c in enumerate(lista):
            self.tabla.setItem(row, 0, QTableWidgetItem(c.empresa))
            self.tabla.setItem(row, 1, QTableWidgetItem(c.nit))
            self.tabla.setItem(row, 2, QTableWidgetItem(c.tipo_cliente.value if hasattr(c.tipo_cliente, 'value') else str(c.tipo_cliente)))
            self.tabla.setItem(row, 3, QTableWidgetItem(c.correo_principal or ""))
            self.tabla.setItem(row, 4, QTableWidgetItem(c.telefono_principal or ""))

    def _filtrar_clientes(self):
        texto = self.filter_bar.txt_buscar.text().strip().lower()
        if not texto:
            self._mostrar_clientes_en_tabla(self.clientes_list)
            return

        filtrados = [
            c for c in self.clientes_list
            if texto in c.empresa.lower() or texto in c.nit.lower() or (c.correo_principal and texto in c.correo_principal.lower())
        ]
        self._mostrar_clientes_en_tabla(filtrados)

    def _on_cliente_seleccionado(self):
        row = self.tabla.currentRow()
        if row < 0 or row >= len(self.clientes_list):
            return

        cliente = self.clientes_list[row]
        info_html = f"""
        <div style="line-height: 1.6;">
            <p><b>Empresa:</b> {cliente.empresa}</p>
            <p><b>NIT:</b> {cliente.nit}</p>
            <p><b>Tipo:</b> {cliente.tipo_cliente.value if hasattr(cliente.tipo_cliente, 'value') else cliente.tipo_cliente}</p>
            <p><b>Correo:</b> {cliente.correo_principal or 'N/A'}</p>
            <p><b>Teléfono:</b> {cliente.telefono_principal or 'N/A'}</p>
            <p><b>Dirección:</b> {cliente.direccion or 'N/A'}</p>
            <p><b>Observaciones:</b> {cliente.observaciones or 'Sin observaciones'}</p>
        </div>
        """
        self.lbl_detalle_info.setText(info_html)
        self.drawer.show()

    def _cerrar_drawer(self):
        self.drawer.hide()

    def _abrir_modal_nuevo_cliente(self):
        dialog = NuevoClienteDialog(self)
        if dialog.exec() == QDialog.Accepted:
            dto = dialog.get_dto()
            if not dto.empresa or not dto.nit or not dto.correo_principal:
                QMessageBox.warning(self, "Campos Requeridos", "Debe diligenciar Empresa, NIT y Correo Principal.")
                return
            try:
                self.controller.crear_cliente(dto, usuario_id=1)
                QMessageBox.information(self, "Éxito", f"Cliente {dto.empresa} creado correctamente.")
                self.cargar_clientes()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"No se pudo crear el cliente: {e}")
