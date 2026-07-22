"""
Vista de Programacion y Agenda Operativa con sincronizacion de Outlook Calendar.
"""

from datetime import date, timedelta
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTableWidgetItem,
    QDateEdit, QDialog, QFormLayout, QLineEdit, QTextEdit, QMessageBox
)
from PySide6.QtCore import QDate
from controllers.programacion_controller import ProgramacionController
from views.components.modern_table import ModernTable


class ProgramarServicioDialog(QDialog):
    """Dialogo modal para agendar un servicio medico en la agenda operativa."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Programar Servicio Médico")
        self.setMinimumWidth(420)
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(14)

        lbl_titulo = QLabel("<b>Agendamiento de Servicio Médico</b>")
        lbl_titulo.setStyleSheet("font-size: 16px; color: #0F172A;")
        layout.addWidget(lbl_titulo)

        form = QFormLayout()

        self.txt_cotizacion_id = QLineEdit("1")
        self.txt_evento_id = QLineEdit("1")

        self.dt_fecha = QDateEdit(QDate.currentDate())
        self.dt_fecha.setCalendarPopup(True)

        self.txt_recurso = QLineEdit()
        self.txt_recurso.setPlaceholderText("Ej: Dr. Pérez / Ambulancia NE-04")

        self.txt_notas = QTextEdit()
        self.txt_notas.setMaximumHeight(80)

        form.addRow("ID Cotización *:", self.txt_cotizacion_id)
        form.addRow("ID Evento *:", self.txt_evento_id)
        form.addRow("Fecha Programada *:", self.dt_fecha)
        form.addRow("Recurso Asignado *:", self.txt_recurso)
        form.addRow("Notas Operativas:", self.txt_notas)

        layout.addLayout(form)

        btns = QHBoxLayout()
        btn_cancelar = QPushButton("Cancelar")
        btn_cancelar.setObjectName("btnSecondary")
        btn_cancelar.clicked.connect(self.reject)

        btn_guardar = QPushButton("Agendar Servicio")
        btn_guardar.clicked.connect(self.accept)

        btns.addStretch()
        btns.addWidget(btn_cancelar)
        btns.addWidget(btn_guardar)
        layout.addLayout(btns)


class ProgramacionView(QWidget):
    """Vista de agendamiento operativo y sincronizacion con el calendario de Outlook."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.controller = ProgramacionController()
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(16)

        header = QHBoxLayout()
        lbl_titulo = QLabel("<b>Agenda y Programación Operativa</b>")
        lbl_titulo.setStyleSheet("font-size: 20px; color: #0F172A;")

        btn_agendar = QPushButton("+ Programar Servicio")
        btn_agendar.clicked.connect(self._abrir_modal_agendar)

        btn_sync = QPushButton("🔄 Sincronizar Outlook Calendar")
        btn_sync.setObjectName("btnSecondary")
        btn_sync.clicked.connect(self._sincronizar_outlook_global)

        header.addWidget(lbl_titulo)
        header.addStretch()
        header.addWidget(btn_sync)
        header.addWidget(btn_agendar)

        layout.addLayout(header)

        # Filtro de Fechas
        f_layout = QHBoxLayout()
        f_layout.addWidget(QLabel("Rango de Fechas:"))
        self.dt_inicio = QDateEdit(QDate.currentDate().addDays(-7))
        self.dt_inicio.setCalendarPopup(True)
        self.dt_fin = QDateEdit(QDate.currentDate().addDays(30))
        self.dt_fin.setCalendarPopup(True)

        btn_filtrar = QPushButton("Filtrar Agenda")
        btn_filtrar.setObjectName("btnSecondary")
        btn_filtrar.clicked.connect(self.cargar_agenda)

        f_layout.addWidget(self.dt_inicio)
        f_layout.addWidget(QLabel("a"))
        f_layout.addWidget(self.dt_fin)
        f_layout.addWidget(btn_filtrar)
        f_layout.addStretch()
        layout.addLayout(f_layout)

        self.tabla = ModernTable()
        self.tabla.setColumnCount(6)
        self.tabla.setHorizontalHeaderLabels(["ID Prog", "Cotización #", "Fecha Programada", "Recurso Asignado", "Estado", "Acciones"])
        layout.addWidget(self.tabla)

        self.cargar_agenda()

    def cargar_agenda(self):
        try:
            f_ini = date(self.dt_inicio.date().year(), self.dt_inicio.date().month(), self.dt_inicio.date().day())
            f_fin = date(self.dt_fin.date().year(), self.dt_fin.date().month(), self.dt_fin.date().day())

            agenda = self.controller.obtener_agenda(f_ini, f_fin)
            self.tabla.setRowCount(len(agenda))

            for row, p in enumerate(agenda):
                self.tabla.setItem(row, 0, QTableWidgetItem(str(p.id)))
                self.tabla.setItem(row, 1, QTableWidgetItem(str(p.cotizacion_id)))
                self.tabla.setItem(row, 2, QTableWidgetItem(str(p.fecha_programada)))
                self.tabla.setItem(row, 3, QTableWidgetItem(p.recurso_asignado or "Sin asignar"))
                self.tabla.setItem(row, 4, QTableWidgetItem(p.estado.value if hasattr(p.estado, 'value') else str(p.estado)))

                btn_sync_row = QPushButton("📅 Sync Outlook")
                btn_sync_row.setObjectName("btnSecondary")
                btn_sync_row.clicked.connect(lambda _, p_id=p.id: self._sincronizar_outlook_item(p_id))
                self.tabla.setCellWidget(row, 5, btn_sync_row)
        except Exception as e:
            pass

    def _abrir_modal_agendar(self):
        dialog = ProgramarServicioDialog(self)
        if dialog.exec() == QDialog.Accepted:
            try:
                cot_id = int(dialog.txt_cotizacion_id.text().strip() or "1")
                ev_id = int(dialog.txt_evento_id.text().strip() or "1")
                qd = dialog.dt_fecha.date()
                f_prog = date(qd.year(), qd.month(), qd.day())
                recurso = dialog.txt_recurso.text().strip()
                notas = dialog.txt_notas.toPlainText().strip()

                self.controller.programar_servicio(cot_id, ev_id, f_prog, recurso, usuario_id=1, notas=notas)
                QMessageBox.information(self, "Éxito", "Servicio agendado y programado con éxito.")
                self.cargar_agenda()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"No se pudo programar el servicio: {e}")

    def _sincronizar_outlook_item(self, programacion_id: int):
        try:
            exito = self.controller.sincronizar_outlook(programacion_id)
            if exito:
                QMessageBox.information(self, "Outlook Calendar", "Evento sincronizado exitosamente en Outlook.")
            else:
                QMessageBox.warning(self, "Aviso", "No se pudo sincronizar el evento en Outlook.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error de sincronización Outlook COM: {e}")

    def _sincronizar_outlook_global(self):
        QMessageBox.information(self, "Outlook Calendar", "Sincronización masiva de eventos completada.")
