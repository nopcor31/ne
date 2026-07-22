"""
Hilo de ejecucion secundario (QThread) para el monitoreo periodico de Alertas.
"""

import time
from PySide6.QtCore import QThread, Signal
from config.settings import settings
from core.session_manager import session_manager
from services.alerta_service import AlertaService
from loguru import logger


class AlertaWorker(QThread):
    """
    Worker en background que evalua reglas de alerta periodicamente
    sin bloquear la interfaz de usuario PySide6.
    """
    # Señal emitida cuando se detectan nuevas alertas
    alertas_actualizadas = Signal(int)  # Emite la cantidad de alertas activas

    def __init__(self, usuario_id: int, parent=None):
        super().__init__(parent)
        self.usuario_id = usuario_id
        self._ejecutando = True

    def run(self) -> None:
        """Ciclo de ejecucion del hilo secundario."""
        logger.info(f"AlertaWorker iniciado para usuario ID {self.usuario_id}")
        while self._ejecutando:
            try:
                with session_manager.session_scope() as session:
                    alerta_svc = AlertaService(session)
                    alerta_svc.evaluar_y_generar_alertas(self.usuario_id)
                    activas = alerta_svc.obtener_alertas_activas(self.usuario_id)
                    cant_activas = len(activas)

                # Emitir señal a la UI
                self.alertas_actualizadas.emit(cant_activas)

            except Exception as exc:
                logger.error(f"Error en evaluacion de AlertaWorker background: {exc}")

            # Esperar el intervalo configurado (300 segundos por defecto)
            for _ in range(settings.INTERVALO_CHECK_ALERTAS_SEGUNDOS):
                if not self._ejecutando:
                    break
                time.sleep(1)

        logger.info("AlertaWorker finalizado correctamente.")

    def detener() -> None:
        """Detiene la ejecucion del hilo de forma segura."""
        self._ejecutando = False
        self.wait()
