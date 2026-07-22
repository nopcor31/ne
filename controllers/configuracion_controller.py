"""
Controlador MVC para la Configuracion del Sistema con señales Qt.
"""

from typing import Optional
from PySide6.QtCore import QObject, Signal, Slot
from core.session_manager import session_manager
from repositories.configuracion_repository import ConfiguracionRepository


class ConfiguracionController(QObject):
    """Controlador para parametros clave-valor de configuracion mediante señales Qt."""

    configuraciones_cargadas = Signal(list)
    configuracion_guardada = Signal(object)
    error_ocurrido = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

    @Slot()
    def obtener_todas(self):
        """Obtiene la lista completa de parametros de configuracion."""
        try:
            with session_manager.session_scope() as session:
                repo = ConfiguracionRepository(session)
                configs = repo.get_all()
                self.configuraciones_cargadas.emit(configs)
                return configs
        except Exception as e:
            self.error_ocurrido.emit(str(e))
            raise

    @Slot(str, object)
    def obtener_valor(self, clave: str, valor_defecto: Optional[str] = None) -> Optional[str]:
        """Obtiene el valor de una variable de configuracion por su clave."""
        try:
            with session_manager.session_scope() as session:
                repo = ConfiguracionRepository(session)
                return repo.obtener_valor(clave, valor_defecto)
        except Exception as e:
            self.error_ocurrido.emit(str(e))
            raise

    @Slot(str, str, object)
    def guardar_valor(self, clave: str, valor: str, descripcion: Optional[str] = None):
        """Establece o actualiza un parametro de configuracion global."""
        try:
            with session_manager.session_scope() as session:
                repo = ConfiguracionRepository(session)
                config = repo.guardar_valor(clave, valor, descripcion)
                self.configuracion_guardada.emit(config)
                return config
        except Exception as e:
            self.error_ocurrido.emit(str(e))
            raise
