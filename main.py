"""
Punto de Entrada Principal de la Aplicación CRM Operativo NE.
"""

import sys
import os
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QFile, QTextStream
from config.logging_config import configurar_logging
from core.database import inicializar_base_datos
from core.session_manager import session_manager
from views.main_window import MainWindow
from models import Ciudad, Festivo, ServicioMedico, Tarifa, Usuario
from core.enums import RolUsuario, TipoDia, HorarioTarifa
from datetime import date
from loguru import logger


def cargar_estilos_qss(app: QApplication) -> None:
    """Carga la hoja de estilos global QSS en la instancia de QApplication."""
    qss_path = os.path.join(os.path.dirname(__file__), "resources", "styles", "main.qss")
    if os.path.exists(qss_path):
        with open(qss_path, "r", encoding="utf-8") as f:
            app.setStyleSheet(f.read())
        logger.info("Estilos QSS cargados correctamente.")


def sembrar_datos_iniciales():
    """Puebla los catalogos base (Ciudades, Festivos, Servicios, Usuario Admin, Tarifas) si la BD esta vacia."""
    with session_manager.session_scope() as session:
        # 1. Usuario Admin
        if not session.query(Usuario).first():
            admin = Usuario(
                nombre_completo="Administrador Comercial",
                email="admin@serviciosmedicosne.com",
                rol=RolUsuario.ADMINISTRADOR,
                activo=True
            )
            session.add(admin)

        # 2. Ciudades Base
        if not session.query(Ciudad).first():
            bogota = Ciudad(nombre="Bogotá", departamento="Cundinamarca")
            medellin = Ciudad(nombre="Medellín", departamento="Antioquia")
            cali = Ciudad(nombre="Cali", departamento="Valle del Cauca")
            session.add_all([bogota, medellin, cali])
            session.flush()

            # 3. Servicios Medicos
            ambulancia_tab = ServicioMedico(
                nombre="Ambulancia TAB (Soporte Básico)",
                codigo="SERV-TAB-01",
                descripcion="Traslado asistencial básico"
            )
            ambulancia_tam = ServicioMedico(
                nombre="Ambulancia TAM (Soporte Avanzado)",
                codigo="SERV-TAM-02",
                descripcion="Traslado asistencial medicalizado"
            )
            evento_medico = ServicioMedico(
                nombre="Atención de Evento / Feria",
                codigo="SERV-EV-03",
                descripcion="Cobertura médica de eventos masivos"
            )
            session.add_all([ambulancia_tab, ambulancia_tam, evento_medico])
            session.flush()

            # 4. Tarifas Base para Bogota
            tarifa_diurna = Tarifa(
                ciudad_id=bogota.id,
                servicio_id=ambulancia_tab.id,
                tipo_dia=TipoDia.ORDINARIO,
                horario=HorarioTarifa.DIURNO,
                valor_hora=150000.0
            )
            tarifa_nocturna = Tarifa(
                ciudad_id=bogota.id,
                servicio_id=ambulancia_tab.id,
                tipo_dia=TipoDia.ORDINARIO,
                horario=HorarioTarifa.NOCTURNO,
                valor_hora=200000.0
            )
            session.add_all([tarifa_diurna, tarifa_nocturna])

        # 5. Festivos Colombia 2026
        if not session.query(Festivo).first():
            festivos_2026 = [
                Festivo(fecha=date(2026, 1, 1), descripcion="Año Nuevo"),
                Festivo(fecha=date(2026, 1, 12), descripcion="Día de los Reyes Magos"),
                Festivo(fecha=date(2026, 3, 23), descripcion="Día de San José"),
                Festivo(fecha=date(2026, 4, 2), descripcion="Jueves Santo"),
                Festivo(fecha=date(2026, 4, 3), descripcion="Viernes Santo"),
                Festivo(fecha=date(2026, 5, 1), descripcion="Día del Trabajo"),
                Festivo(fecha=date(2026, 5, 18), descripcion="Ascensión del Señor"),
                Festivo(fecha=date(2026, 6, 8), descripcion="Corpus Christi"),
                Festivo(fecha=date(2026, 6, 15), descripcion="Sagrado Corazón"),
                Festivo(fecha=date(2026, 6, 29), descripcion="San Pedro y San Pablo"),
                Festivo(fecha=date(2026, 7, 20), descripcion="Día de la Independencia"),
                Festivo(fecha=date(2026, 8, 7), descripcion="Batalla de Boyacá"),
                Festivo(fecha=date(2026, 8, 17), descripcion="La Asunción de la Virgen"),
                Festivo(fecha=date(2026, 10, 12), descripcion="Día de la Raza"),
                Festivo(fecha=date(2026, 11, 2), descripcion="Todos los Santos"),
                Festivo(fecha=date(2026, 11, 16), descripcion="Independencia de Cartagena"),
                Festivo(fecha=date(2026, 12, 8), descripcion="Inmaculada Concepción"),
                Festivo(fecha=date(2026, 12, 25), descripcion="Navidad"),
            ]
            session.add_all(festivos_2026)

        logger.info("Catálogos iniciales validados/sembrados exitosamente.")


def main():
    """Inicializacion global del sistema."""
    configurar_logging()
    logger.info("Iniciando CRM Operativo — Servicios Médicos NE...")

    # Inicializar Base de Datos SQLite WAL
    inicializar_base_datos()
    sembrar_datos_iniciales()

    # Iniciar Aplicacion PySide6 UI
    app = QApplication(sys.argv)
    cargar_estilos_qss(app)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
